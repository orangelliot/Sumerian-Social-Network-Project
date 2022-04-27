
# Elliot Fisk, collect names

import os
from multiprocessing import Process
import multiprocessing
from Database.SQLfuncs import SQLfuncs
class MultiNameGrabber(object):

    processes = list()
    tabletsProcessed = 0

    def __init__(self, path):
        self.path = path

    def namesToDB(self):
        numProc = multiprocessing.cpu_count()
        tablets = os.listdir(self.path)
        numTablets = len(tablets)
        threadSize = numTablets/numProc
        pos = 0
        for index in range(numProc - 1):
            p = Process(target=self.thread_function, args=(self, index, tablets[pos, pos + threadSize],))
            self.processes.append(p)
            pos += threadSize
        p = Process(target=self.thread_function, args=(self, numProc, tablets[pos, numTablets - 1],))
        self.processes.append(p)

        for process in self.processes:
            process.start()

        while self.tabletsProcessed <= numTablets:
            print("%d/%d" % (self.tabletsProcessed, numTablets), end="\r")

        for process in self.processes:
            process.join()
        
        

    def thread_function(self, name, tablets):
        self.tabletsProcessed = 0
        db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
        for tabid in tablets:
            self.tabletsProcessed += 1
            #open each tablet
            tab = open(self.path + tabid, 'r', encoding='utf-8')
            #start read
            currentLine = tab.readline()
            placeName = False
            #continue until end of tablet
            while currentLine != '':
                #split line around tab and tokenize
                tokenLine = currentLine.split('\t')
                if(currentLine.find("[place]") != -1):
                    placeName = True
                if(currentLine.find("\tPN\n") != -1):
                    if(placeName):
                        #catch placeNames and dont add them to the database
                        placeName = False
                    else:
                        #if PN then add to sql
                        db.addNameToTab(tokenLine[1], tabid[0:7])
                currentLine = tab.readline()
        print('Thread ' + name + ' finished\n')