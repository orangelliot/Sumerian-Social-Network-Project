import multiprocessing as mp
import pandas as pd
from Database.SQLfuncs import SQLfuncs

CULLING_DEPTH = 100

def enqueue_edges(names, q, cpu, progress):
    progress[cpu - 1] = 0
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    
    for name in names:
        progress[cpu - 1] += 1
        query = f"select distinct tabids{CULLING_DEPTH}.seqid from rawnames join tabids{CULLING_DEPTH} where rawnames.tabid = tabids{CULLING_DEPTH}.tabid and name = \'" + name + "\';"
        tabs_with_name = db.execute_select(query)

        for i in range(len(tabs_with_name)):
            tabs_with_name[i] = tabs_with_name[i][0]
    
        while len(tabs_with_name) > 1:
            edge_progress = 0
            sup_tab = tabs_with_name.pop()
            for sub_tab in tabs_with_name:
                edge_progress += 1
                edge = [sup_tab, sub_tab]
                if sup_tab > sub_tab:
                    edge = [sub_tab, sup_tab]
                q.put(edge)

def consume_queue(q, finish, num_tabs):
    net_df = pd.read_csv(f'tablet_net{CULLING_DEPTH}f.csv')

    while finish.value == 0:
        if not q.empty():
            edge = q.get()
            try:
                net_df.iat[idxe(edge, num_tabs), 2] += 1
            except:
                print('tried to index the edge ' + str(edge) + ' out of bounds\n')

    net_df.to_csv(f'tablet_net{CULLING_DEPTH}.csv', header=True, mode='a', index=False)

def idxe(edge, num_tabs):
    start = num_tabs - edge[0] + 1
    end = num_tabs - 1
    return int(((-(1/2))*(start - end - 1)*(start + end)) + (edge[1] - edge[0]))


if __name__ == '__main__':
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    progress = mp.Array('i', range(n_cpus))
    procs = list()
    names = db.execute_select(f'select distinct name from rawnames join tabids{CULLING_DEPTH} where rawnames.tabid = tabids{CULLING_DEPTH}.tabid;')
    for i in range(len(names)):
        names[i] = names[i][0]
    num_tabs = db.execute_select(f'select count(tabid) from tabids{CULLING_DEPTH};')[0][0]
    n_names = len(names)
    thread_size = int(n_names/n_cpus)
    pos = 0
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=enqueue_edges, args=(names[pos:(pos + thread_size - 1)], q, cpu, progress,))
        procs.append(proc)
        pos += thread_size
        #print('appended process covering names ' + str(pos) + ' through ' + str(pos + thread_size - 1) + ' to the process list')
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
        print("%d/%d queue size = %d" % (sum, (n_names - 100), q.qsize()), end='\r')

    for p in procs:
        p.join()
    
    cq_finish.value = 1
    print('started cq finish routine')
    cq_proc.join()