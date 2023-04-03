from Database.SQLfuncs import SQLfuncs
import numpy as np
import pandas as pd
import multiprocessing as mp
import ctypes

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

def thread_function(tuplestoinsert, cpu, progress):
    progress[cpu - 1] = 0
    for tuple in tuplestoinsert:
        progress[cpu - 1] += 1
        db.execute_insert(f"insert into bestyearsfixedfixed values ('{tuple[0]}', '{tuple[1]}', '{tuple[2]}');")

if __name__ == '__main__':
    table = db.execute_select('select * from bestyearsfixed order by tabid;')

    #print(table)

    new = []
    skip = 0

    for i in range(len(table)):
        if skip == 0:
            if i < len(table) - 1:
                best = table[i]
                j = 1
                while table[i][1] == table[i+j][1]:
                    if best[2] > table[i+j][2]:
                        best = table[i+j]
                    j += 1
                    skip += 1
                new.append(best)
            else:
                new.append(table[i])
        else:
            skip -= 1

    sum = 0
    n_cpus = mp.cpu_count()
    pos = 0
    thread_size = int(len(new)/n_cpus)
    print(thread_size)
    procs = []
    progress = mp.Array(ctypes.c_int, range(n_cpus))

    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=thread_function, args=(new[pos:(pos + thread_size - 1)], cpu, progress))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=thread_function, args=(new[pos:(len(new) - 1)], n_cpus, progress))
    procs.append(proc)

    for p in procs:
        p.start()

    sum = 0
    while(sum < len(new)):
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
            print("%d/%d" % (sum, len(new)), end='\r')

        for p in procs:
            p.join()