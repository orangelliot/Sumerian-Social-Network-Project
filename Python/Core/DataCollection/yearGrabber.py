import os
import re
import threading
from Database.SQLfuncs import SQLfuncs

class YearGrabber(object):
    
    def __init__(self, path):
        self.path = path
        self.tablets = os.listdir(path)

    def yearsToDB(self):
        db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
        currentTablet = 0
        numTablets = len(self.tablets)
        for tabid in self.tablets:
            print("%d/%d" % (currentTablet, numTablets), end="\r")
            currentTablet += 1
            #open each tablet
            tab = open(self.path + tabid, 'r', encoding='utf-8')
            currentLine = tab.readline()
            buf = "mu "
            yearCount = 0
            while currentLine != '':
                if(currentLine.find("[year]") != -1):
                    currentLine = tab.readline()
                    end = False
                    while currentLine != '' and not end:
                        buf += re.split(' |\t', currentLine)[1]
                        buf += ' '
                        end = (-1 != currentLine.find("\tV"))
                        currentLine = tab.readline()
                    end = False
                    #add year to db
                    db.addYearToTab(buf, tabid[0:7])
                    buf = "mu "
                    yearCount += 1
                    continue
                currentLine = tab.readline()
        print("years finished")
                
