import multiprocessing as mp
import numpy as np
import pandas as pd
from Database.SQLfuncs import SQLfuncs

MIN_COUNT = 10



if __name__ == '__main__':
    db = SQLfuncs('localhost', 'root', 'admin2019')
    n_cpus = mp.cpu_count()
    q = mp.Queue()
    progress = mp.Array('i', range(n_cpus))
    procs = list()

    try:
        db.execute_insert('create temporary table ambigtabs select rawyears.tabid, rawnames.name, metanames.count, metayears.bestyear, metayears.similarity from rawyears join rawnames on rawyears.tabid=rawnames.tabid join metanames on rawnames.name=metanames.name join metayears on rawyears.year=metayears.year where metayears.bestyear like \'ambiguous%\' order by rawyears.tabid;')
    except:
        print('fard you')
    tablist = db.execute_select('select * from ambigtabs group by tabid')
    
    print(tablist[0])