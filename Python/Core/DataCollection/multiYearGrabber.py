# Multi Year Grabber
# May 2022
# Elliot Fisk
# ---------------
# TODO synopsis and comments v below v

import os
import psutil
import multiprocessing as mp
from Database.SQLfuncs import SQLfuncs

import re

def thread_function(path, tablets, cpu, progress):
    progress[cpu - 1] = 0
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    for tabid in tablets:
        progress[cpu - 1] += 1
        tab = open(path + tabid, 'r', encoding='utf-8')
        current_line = tab.readline()

        buf = "mu "
        while current_line != '':
            if current_line.find("[year]") != -1:
                current_line = tab.readline()
                end = False
                while current_line != '' and not end:
                    buf += re.split(' |\t', current_line)[1]
                    buf += ' '
                    end = (-1 != current_line.find("\tV"))
                    current_line = tab.readline()
                db.execute_insert('insert into rawyears values (%s, %s);' % buf, tabid[0:7])
                buf = "mu "
            else:
                current_line = tab.readline()

path = os.getcwd() + '/Dataset/Translated/'

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
        print("started new thread on tablets[%d,%d]" % (pos, (pos + thread_size - 1)))
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