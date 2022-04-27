# Elliot Fisk, collect names

import os
import threading
from Database.SQLfuncs import SQLfuncs
class NameGrabber(object):

    def __init__(self, path):
        self.path = path
        self.tablets = os.listdir(path)

    def namesToDB(self):
        db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
        currentTablet = 0
        numTablets = len(self.tablets)
        for tabid in self.tablets:
            print("%d/%d" % (currentTablet, numTablets), end="\r")
            currentTablet += 1
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
        print("names finished")