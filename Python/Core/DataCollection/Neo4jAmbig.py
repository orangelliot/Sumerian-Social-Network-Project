import multiprocessing as mp
import numpy as np
import pandas as pd
import time
from neo4j import GraphDatabase as gd
from Database.SQLfuncs import SQLfuncs

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

def namesQueue(nameset, q, p, cpu):
    print(f'started namesqueue for cpu {cpu}')
    p[cpu - 1] = 0
    for name in nameset:
        q.put(f'create (n:Name {{name:\'{name[0]}\'}})')
        p[cpu - 1] += 1

def tabsQueue(tabsplit, q, p, cpu):
    print(f'started tabsqueue for cpu {cpu}')
    p[cpu - 1] = 0
    for tablet in tabsplit:
        namelist = ''
        for tuple in tablet:
            namelist += f'n.name=\'{tuple[1]}\' or '
        namelist = namelist[:-4]
        q.put(f'create (t:Tablet {{tabid:\'{tablet[-1][0]}\', year:\'{tablet[-1][2]}\', sim:{tablet[-1][3]}}}) with t match (n:Name) where {namelist} create (t)-[r:HasName]->(n)')
        p[cpu - 1] += 1

def consumeQ(q, p, nnames, ntabs, switch):
    print('started consumeq')
    neodriver = gd.driver(URI, auth=AUTH)
    n_cpus = mp.cpu_count()
    while True:
        neodriver.execute_query(q.get())
        sum = 0
        for i in range(n_cpus):
            sum += p[i]
        if switch.value == 1:
            print("%d/%d        " % (sum, ntabs), end='\r')
        else:
            print("%d/%d        " % (sum, nnames), end='\r')
        if q.qsize() == 0 and switch.value != 2:
            for i in range(5):
                time.sleep(1)
                print(f'empty for {i+1} seconds                         ')
                if i==4:
                    print('transfer complete                            ')
                    quit()

def main():
    sqldriver = SQLfuncs('localhost', 'root', 'admin2019')
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    p = mp.Array('i', range(n_cpus))
    switch = mp.Value('i', 0)

    tabinfo = sqldriver.execute_select('select tabid, name, bestyear, similarity from fulltabs order by tabid;')
    tabsplit = np.split(tabinfo, np.unique(tabinfo[:, 0], return_index=True)[-1][1:])
    nameset = sqldriver.execute_select('select distinct name from fulltabs;')

    nnames = len(nameset)
    ntabs = len(tabsplit)

    tabthreadsize = int(ntabs/n_cpus)
    # namethreadsize = int(nnames/n_cpus)

    # pos = 0
    # procs = list()
    # for cpu in range(n_cpus - 1):
    #     proc = mp.Process(target=namesQueue, args=(nameset[pos:(pos+namethreadsize)], q, p, cpu))
    #     procs.append(proc)
    #     pos += namethreadsize
    # proc = mp.Process(target=namesQueue, args=(nameset[pos:], q, p, n_cpus - 1))
    # procs.append(proc)

    # for proc in procs:
    #     proc.start()
    
    # c = mp.Process(target=consumeQ, args=(q, p, nnames, ntabs, switch))
    # c.start()

    # for proc in procs:
    #     proc.join()
    
    print('switching to tablets')
    switch.value = 2

    c = mp.Process(target=consumeQ, args=(q, p, nnames, ntabs, switch))
    c.start()

    pos = 0
    procs = list()
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=tabsQueue, args=(tabsplit[pos:(pos+tabthreadsize)], q, p, cpu))
        procs.append(proc)
        pos += tabthreadsize
    proc = mp.Process(target=tabsQueue, args=(tabsplit[pos:], q, p, n_cpus - 1))
    procs.append(proc)

    for proc in procs:
        proc.start()
    
    switch.value = 1
    
    for proc in procs:
        proc.join()

    c.join()

if __name__ == '__main__':
    main()