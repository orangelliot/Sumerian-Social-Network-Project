import multiprocessing as mp
import numpy as np
import pandas as pd
from Database.SQLfuncs import SQLfuncs

MIN_COUNT = 10

def enqueueEdges(names):
    db = SQLfuncs('localhost', 'root', 'admin2019')
    for name in names:
        ambig = db.execute_select(f'select tabid, count, similarity from fulltabs where fulltabs.name=\'{name}\' and fulltabs.bestyear like \'ambig%\';')
        gen = db.execute_select(f'select tabid, count, similarity from fulltabs where fulltabs.name=\'{name}\' and fulltabs.bestyear not like \'ambig%\';')

if __name__ == '__main__':
    db = SQLfuncs('localhost', 'root', 'admin2019')
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    p = mp.Array('i', range(n_cpus))

    try:
        db.execute_insert('create temporary table fulltabs select rawyears.tabid, rawnames.name, metanames.count, metayears.bestyear, metayears.similarity from rawyears join rawnames on rawyears.tabid=rawnames.tabid join metanames on rawnames.name=metanames.name join metayears on rawyears.year=metayears.year order by rawyears.tabid;')
    except:
        print('skipped table creation')
    ambig_names = db.execute_select('select distinct name from ambigtabs;')
    
    batch_size = len(ambig_names)/n_cpus
    pos = 0

    procs = list()
    for i in range(n_cpus):
        proc = mp.Process()