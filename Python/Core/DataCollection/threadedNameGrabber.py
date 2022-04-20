
# Elliot Fisk, collect names

import os
import threading
from Database.SQLfuncs import SQLfuncs
class NameGrabber(object):

    tabletsProcessed = 0
    threads = list()

    def namesToDB(self, numThreads, path):
        self.path = path
        tablets = os.listdir(self.path)
        numTablets = len(tablets)
        threadSize = numTablets/numThreads
        pos = 0
        for index in range(numThreads - 1):
            th = threading.Thread(target=self.thread_function, args=(index, self, tablets[pos, pos + threadSize], self.path))
            th.start()
            self.threads.append(th)
            pos += threadSize
        th = threading.Thread(target=self.thread_function, args=(numThreads, self, tablets[pos, numTablets - 1], self.path))
        th.start()
        self.threads.append(th)
        


    def thread_function(name, self, tablets, path):
        db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
        for tabid in tablets:
            self.tabletsProcessed += 1
            #open each tablet
            tab = open(path + tabid, 'r', encoding='utf-8')
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