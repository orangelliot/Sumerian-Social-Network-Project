import multiprocessing as mp
import os
import psutil

def testThread(cpu, progress):
    proc = psutil.Process()
    proc.cpu_affinity([cpu])
    progress[cpu] = 0
    for j in range(10000):
        progress[cpu] += 1

if __name__ == '__main__':
    n_cpus = psutil.cpu_count()
    progress = mp.Array('i', range(n_cpus))
    procs = list()
    sumProg = 0
    for cpu in range(n_cpus):
        p = mp.Process(target=testThread, args=(cpu,progress,)) #create the child process using defauly spawn() protocol
        p.start() #start the child
        procs.append(p) #add it to list of running procs

    sum = 0
    while sum < 160000:
        sum = 0
        for i in range(n_cpus):
            sum += progress[i]
        print(sum, end='\r')
        #print("%d/%d" % (progress.value, 160000), end='\r')

    for p in procs:
        p.join()