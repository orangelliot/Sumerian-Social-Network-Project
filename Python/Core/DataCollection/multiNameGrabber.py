
# Elliot Fisk, collect names

import os
import multiprocessing as mp
import psutil
from Database.SQLfuncs import SQLfuncs

path = os.getcwd() + '/Dataset/Translated/'

def thread_function(path, tablets, cpu, progress):
    progress[cpu - 1] = 0
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    for tabid in tablets:
        progress[cpu - 1] += 1
        tab = open(path + tabid, 'r', encoding='utf-8')
        current_line = tab.readline()

        is_pn = False
        while current_line != '':
            token_line = current_line.split('\t')
            if(current_line.find("[place]") != -1):
                is_pn = True
            if(current_line.find("\tPN\n") != -1):
                if(is_pn):
                    is_pn = False
                else:
                    db.execute_insert('insert into rawnames values (%s, %s);' % token_line[1], tabid[0:7])
            current_line = tab.readline()

if __name__ == '__main__':
    n_cpus = psutil.cpu_count()
    procs = list()
    progress = mp.Array('i', range(n_cpus))
    tablets = os.listdir(path)
    num_tablets = len(tablets)
    thread_size = int(num_tablets/n_cpus)
    pos = 0
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=thread_function, args=(path, tablets[pos:(pos + thread_size - 1)], cpu, progress,))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=thread_function, args=(path, tablets[pos:(num_tablets - 1)], n_cpus, progress,))
    procs.append(proc)

    for p in procs:
        p.start()

    sum = 0
    while sum < num_tablets:
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print("%d/%d" % (sum, num_tablets), end='\r')

    for p in procs:
        p.join()