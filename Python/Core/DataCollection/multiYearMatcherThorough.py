#Elliot Fisk: find closest match for each tablet's year

import os
import multiprocessing as mp
import psutil
import pandas as pd
from Database.SQLfuncs import SQLfuncs

from difflib import SequenceMatcher

YEARS_START = 0
YEARS_END = 5000

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
cdli_years = db.execute_select('select * from cdliyears;')
for i in range(len(cdli_years)):
    cdli_years[i] = cdli_years[i][:2]

def get_sim_metric(s1, s2):
    ssl = len(s1)
    if ssl < len(s2):
        best = 0
        for i in range(len(s2) - ssl):
            segsim = SequenceMatcher(None, s1, s2[i:i+ssl]).ratio()
            if segsim > best:
                best = segsim
        return best
    return SequenceMatcher(None, s1, s2).ratio()

def match_year(year_name):
    best_year = ''
    sim_metric = 0
    for row in range(len(cdli_years)):
        cur_year = cdli_years[row][0]
        temp = get_sim_metric(cur_year, year_name)
        if  temp >= sim_metric:
            sim_metric = temp
            best_year = cdli_years[row][1]
    return best_year, sim_metric

def thread_function(years, cpu, progress):
    progress[cpu - 1] = 0
    #db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    for tuple in years:
        progress[cpu - 1] += 1
        row = 0
        best_sim = 0
        best_year = 'start'
        year = tuple[0]
        tablet = tuple[1]
        for i in range(len(cdli_years)):
            temp_year, similarity = match_year(year)
            if similarity >= best_sim:
                best_year = temp_year
                best_sim = similarity
        best_sim *= 100.0
        db.execute_insert(f'insert into bestyearsfixed values (\"{best_year}\", \"{tablet}\", {int(best_sim)});')
        row += 1

if __name__ == '__main__':
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    n_cpus = psutil.cpu_count()
    procs = list()
    progress = mp.Array('i', range(n_cpus))
    years = db.execute_select("select * from rawyearsfixed group by tabid;")
    years = years[YEARS_START:YEARS_END]
    num_years = len(years)
    thread_size = int(num_years/n_cpus)
    pos = 0
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=thread_function, args=(years[pos:(pos + thread_size - 1)], cpu, progress,))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=thread_function, args=(years[pos:(num_years - 1)], n_cpus, progress,))
    procs.append(proc)

    for p in procs:
        p.start()

    sum = 0
    while sum < num_years - 150:
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print("%d/%d" % (sum, num_years), end='\r')

    for p in procs:
        p.join()