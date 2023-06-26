#Elliot Fisk: create CSV edgelist file for tracking shared names as edge weights

import multiprocessing as mp
import numpy as np
import pandas as pd
from Database.SQLfuncs import SQLfuncs

CULLING_SIZE = 1000

# calculate edges and add them to a queue to be written to the main file
def enqueue_edges(names, q, cpu, progress):
    progress[cpu - 1] = 0
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

    # create string for later use in query
    names_string = '('
    for name in names:
        names_string = f"{names_string}'{name}',"
    names_string = names_string[:-1]
    names_string += ')'
    
    # query returns seqids for tablets from ambignames with a name in names
    ambig_tabs = db.execute_select(f"select tabids.seqid from (ambigtabs{CULLING_SIZE} join tabids on ambigtabs{CULLING_SIZE}.tabid = tabids.tabid) join rawnames on ambigtabs{CULLING_SIZE}.tabid = rawnames.tabid where name in {names_string};")
    for i in range(len(ambig_tabs)):
        ambig_tabs[i] = ambig_tabs[i][0]

    # generate edges loop
    for name in names:
        progress[cpu - 1] += 1

        # get all tablets with name 'name'
        query = f"select distinct tabids{CULLING_SIZE}.seqid from rawnames join tabids{CULLING_SIZE} where rawnames.tabid = tabids{CULLING_SIZE}.tabid and name = \'" + name + "\';"
        tabs_with_name = db.execute_select(query)

        for i in range(len(tabs_with_name)):
            tabs_with_name[i] = tabs_with_name[i][0]

        # main loop to generate edges
        while len(ambig_tabs) > 1:
            sup_tab = ambig_tabs.pop()
            for sub_tab in tabs_with_name:
                edge = [sup_tab, sub_tab]
                if sup_tab != sub_tab:
                    q.put(edge)

def consume_queue(q, finish, num_tabs):
    net_nparray = np.genfromtxt(f'ambig_tablet_net{CULLING_SIZE}f.csv', delimiter=',')
    ambig_tabs = net_nparray[:, 0]
    ambig_tabs = np.unique(ambig_tabs)
    for i in range(len(ambig_tabs)):
        ambig_tabs[i] = int(ambig_tabs[i])

    while finish.value == 0:
        if not q.empty():
            edge = q.get()
            try:
                csv_idx = idxe(edge, num_tabs, ambig_tabs)
                net_nparray[csv_idx][2] += 1
            except:
                print('tried to index the edge ' + str(edge) + ' out of bounds at ' + str(csv_idx) + '\n')

    net_df = pd.DataFrame(net_nparray, columns = ['tab1', 'tab2', 'shared_names','tab2_year'], dtype='int')
    net_df.to_csv(f'ambig_tablet_net{CULLING_SIZE}.csv', header=True, mode='a', index=False)

def idxe(edge, num_tabs, ambig_tabs):
    idxezero = np.where(ambig_tabs == int(edge[0]))[0][0]
    return idxezero * num_tabs + edge[1]

if __name__ == '__main__':
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    progress = mp.Array('i', range(n_cpus))
    procs = list()
    # select all the names on ambig tabs
    names = db.execute_select(f'select distinct name from ambigtabs{CULLING_SIZE} join (rawnames join tabids on rawnames.tabid = tabids.tabid) where ambigtabs{CULLING_SIZE}.tabid = tabids.tabid;')
    for i in range(len(names)):
        names[i] = names[i][0]
    num_tabs = db.execute_select(f'select count(tabid) from tabids{CULLING_SIZE};')[0][0]
    n_names = len(names)
    thread_size = int(n_names/n_cpus)
    pos = 0
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
    while sum < (n_names - 10) or q.qsize() > 0:
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print("%d/%d queue size = %d               " % (sum, (n_names), q.qsize()), end='\r')

    for p in procs:
        p.join()
    
    cq_finish.value = 1
    print('\nstarted cq finish routine')
    cq_proc.join()