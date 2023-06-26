# MultiCSV Network Creator
# October 2022
# Elliot Fisk
# ---------------
# creates a CSV edgelist file for tracking shared names as edge weights

import math
import multiprocessing as mp
import numpy as np
import pandas as pd
from Database.SQLfuncs import SQLfuncs

# maximum allowed edge count for any name
CULLING_SIZE = 1000

# calculate edges and add them to a queue to be written to the main file
def enqueue_edges(names, q, cpu, progress):
    progress[cpu - 1] = 0
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

    # for each given name
    for name in names:
        progress[cpu - 1] += 1
        # get all the tablets which share 'name' from tablets in tabids{CULLING_SIZE}
        query = f"select distinct tabids{CULLING_SIZE}.seqid from rawnames join tabids{CULLING_SIZE} where rawnames.tabid = tabids{CULLING_SIZE}.tabid and name = \'" + name + "\';"
        tabs_with_name = db.execute_select(query)

        # clean up output of execute_select
        for i in range(len(tabs_with_name)):
            tabs_with_name[i] = tabs_with_name[i][0]
    
        # generate one edge between all tablets in tabs_with_name and add them to the queue
        while len(tabs_with_name) > 1:
            edge_progress = 0
            sup_tab = tabs_with_name.pop()
            for sub_tab in tabs_with_name:
                edge_progress += 1
                edge = [sup_tab, sub_tab]
                if sup_tab > sub_tab:
                    edge = [sub_tab, sup_tab]
                q.put(edge)

# consumes the edge queue created by enqueue_edges
def consume_queue(q, finish, num_tabs):

    # creates an nparray based on a csv with the appropriate format
    net_nparray = np.genfromtxt(f'tablet_net{CULLING_SIZE}f.csv', delimiter=',')
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

    # match best year for all tablets at CULLING_SIZE with the appropriate year in cdli and return a table containing seqid, which is a tablet id, and seqnum, which is a year id
    tab_years = db.execute_select(f'select seqid, seqnum from tabids{CULLING_SIZE} left join (bestyears left join cdliyears on bestyears.year = cdliyears.kingnum) on tabids{CULLING_SIZE}.tabid = bestyears.tabid;')
    for i in range(len(tab_years)):
        tab_years[i] = tab_years[i][:2]

    # finish is controlled in main
    while finish.value == 0:
        # pull edge from queue
        if not q.empty():
            edge = q.get()
            year_diff = -1
            
            # calculate the year difference between both tablets in edge
            if tab_years[edge[0] - 1][1] != None and tab_years[edge[1] - 1][1] != None:
                year_diff = tab_years[edge[0] - 1][1] - tab_years[edge[1] - 1][1]
            
            # add one edge nparray net
            try:
                csv_idx = idxe(edge, num_tabs)
                net_nparray[csv_idx][2] += 1
                net_nparray[csv_idx][3] = year_diff
            except:
                print('tried to index the edge ' + str(edge) + ' out of bounds\n')

    # save net to CSV
    net_df = pd.DataFrame(net_nparray, columns = ['tab1', 'tab2', 'shared_names', 'year_diff'], dtype='int')
    net_df.to_csv(f'tablet_net{CULLING_SIZE}.csv', header=True, mode='a', index=False)

# find index in net_nparray of a given edge
def idxe(edge, num_tabs):
    start = num_tabs - edge[0] + 1
    end = num_tabs - 1
    return int(((-(1/2))*(start - end - 1)*(start + end)) + (edge[1] - edge[0]))

if __name__ == '__main__':
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    creatable = f'create table #tabids{CULLING_SIZE} (select C.name as Name, C.tabid as Tabid, D.count as Count from (select distinct name, tabid from rawnamesclean order by tabid) as C inner join (select * from (select A.name, count(A.name) as count from (select distinct name, tabid from rawnamesclean order by tabid) as A group by A.name) as B where B.count < {CULLING_SIZE} and B.count > 1) as D on C.name = D.name);'
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    progress = mp.Array('i', range(n_cpus))
    procs = list()
    # get all names from tabids{CULLING_SIZE}
    names = db.execute_select(f'select distinct name from rawnames join tabids{CULLING_SIZE} where rawnames.tabid = tabids{CULLING_SIZE}.tabid;')
    for i in range(len(names)):
        names[i] = names[i][0]
    num_tabs = db.execute_select(f'select count(tabid) from tabids{CULLING_SIZE};')[0][0]
    n_names = len(names)
    thread_size = int(n_names/n_cpus)
    pos = 0
    # distribute work
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=enqueue_edges, args=(names[pos:(pos + thread_size - 1)], q, cpu, progress,))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=enqueue_edges, args=(names[pos:(n_names - 1)], q, n_cpus, progress,))
    procs.append(proc)

    for p in procs:
        p.start()
    print('started processes')

    cq_finish = mp.Value('i', 0)
    cq_proc = mp.Process(target=consume_queue, args=(q, cq_finish, num_tabs,), daemon=True)
    cq_proc.start()

    print('started consumer')

    sum = 0
    while sum < (n_names - 100) or q.qsize() > 0:
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print("%d/%d queue size = %d               " % (sum, (n_names - 100), q.qsize()), end='\r')

    for p in procs:
        p.join()
    
    # once all names have been processed according to progress variable, signal consumer to stop looping
    cq_finish.value = 1
    print('\nstarted cq finish routine')
    cq_proc.join()