#Elliot Fisk: find closest match for each tablet's year

import multiprocessing as mp
import psutil
import ctypes
from Database.SQLfuncs import SQLfuncs
from difflib import SequenceMatcher

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

def match_year(year_name, cdli_years):
    best_year = ''
    sim_metric = 0
    for row in range(len(cdli_years)):
        cur_year = cdli_years[row][2]
        temp = get_sim_metric(cur_year, year_name)
        if  temp >= sim_metric:
            sim_metric = temp
            best_year = cdli_years[row][1]
    return best_year, sim_metric

def thread_function(years, cpu, progress, queue, cdli_years):
    progress[cpu - 1] = 0
    for tuple in years:
        progress[cpu] += 1
        best_sim = 0
        best_year = 'start'
        year = tuple[0]
        for i in range(len(cdli_years)):
            temp_year, similarity = match_year(year, cdli_years)
            if similarity >= best_sim:
                best_year = temp_year
                best_sim = similarity
        best_sim *= 100.0
        queue.put(f'update metayears set bestyear = \'' + best_year + '\', similarity = ' + str(best_sim) + ' where year = \'' + year + '\';')

def consume(queue, progress, num_years):
    n_cpus = psutil.cpu_count()
    db = SQLfuncs('localhost', 'root', 'admin2019')
    sum = 0
    while queue.qsize() > 0 or sum < num_years:
        if(queue.qsize() > 0):
            db.execute_insert(queue.get())
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print("%d/%d" % (sum, num_years), end='\r')

if __name__ == '__main__':
    db = SQLfuncs('localhost', 'root', 'admin2019')
    cdli_years = db.execute_select('select * from cdliyears;')
    n_cpus = psutil.cpu_count()
    print("n_cpus = " + str(n_cpus))
    procs = []
    progress = mp.Array(ctypes.c_int, range(n_cpus))
    queue = mp.Queue()
    years = db.execute_select("select * from metayears where bestyear is null;")
    db.close()
    num_years = len(years)
    thread_size = int(num_years/n_cpus)
    pos = 0
    for cpu in range(n_cpus - 1):
        proc = mp.Process(target=thread_function, args=(years[pos:(pos + thread_size - 1)], cpu, progress, queue, cdli_years))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=thread_function, args=(years[pos:(num_years - 1)], n_cpus - 1, progress, queue, cdli_years))
    procs.append(proc)
    procs.append(mp.Process(target=consume, daemon=True, args=(queue, progress, num_years)))

    for p in procs:
        p.start()

    for p in procs:
        p.join()