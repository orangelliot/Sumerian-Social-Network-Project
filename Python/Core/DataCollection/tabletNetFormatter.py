# Tablet Net Formatter
# October 2022
# Elliot Fisk
# ---------------
# creates an empty formatted csv net with all possible edges but no weights

import multiprocessing as mp
import os
import csv
from Database.SQLfuncs import SQLfuncs
import pandas as pd

def format_producer(incl_set, excl_set, send):
    print(f'started {os.getpid()} on {len(incl_set)} tablets')
    thread_df = pd.DataFrame(columns=('incl_tab', 'excl_tab', 'edge_count', 'year', 'name_dist_mod', 'name_com_mod'))
    for i in range(len(incl_set)):
        for j in range(len(excl_set)):
            new_row = {'incl_tab':incl_set[i][0], 'excl_tab':excl_set[j][0], 'edge_count':0, 'year':-1, 'name_dist_mod':-1, 'name_com_mod':-1}
            thread_df.loc[len(thread_df)] = new_row
        print(f'{os.getpid()} finished {i}/{len(incl_set)} tablets')
    send.send(thread_df)
    print(f'finished {os.getpid()}')

if __name__=='__main__':
    db = SQLfuncs('localhost', 'root', 'admin2019')

    incl_set = db.execute_select('select distinct seqid from fulltabs where bestyear like \'ambig%\';')
    excl_set = db.execute_select('select distinct seqid from fulltabs where bestyear not like \'ambig%\' and name in (select name from metanames where count > 1 and name not like \'-%\');')

    giga_df = pd.DataFrame(columns=('incl_tab', 'excl_tab', 'edge_count', 'year', 'name_dist_mod', 'year_dist_mod', 'name_com_mod'))
    thread_size = int(len(incl_set)/16)
    pipes = list(mp.Pipe() for i in range(16))
    procs = list()
    pos = 0
    for cpu in range(15):
        proc = mp.Process(target=format_producer, args=(incl_set[pos:(pos + thread_size - 1)], excl_set, pipes[cpu][1],))
        procs.append(proc)
        pos += thread_size
    proc = mp.Process(target=format_producer, args=(incl_set[pos:len(incl_set)-1], excl_set, pipes[15][1],))
    procs.append(proc)

    for p in procs:
        p.start()
    print('started processes')

    for pipe in pipes:
        pd.concat([giga_df, pipe[0].recv()], ignore_index=True)
    
    giga_df.to_csv('net_format', index=False)