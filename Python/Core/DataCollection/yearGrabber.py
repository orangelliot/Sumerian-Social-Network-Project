import os
import re
from Database.SQLfuncs import SQLfuncs

class YearGrabber(object):
    
    def __init__(self, path):
        self.path = path

    def yearsToSheet(self):
        db = SQLfuncs('10.0.0.108', 'elliot', 'password')
        tablets = os.listdir(self.path)
        row = 2
        for tablet in tablets:
            #open each tablet
            tab = open(self.path + tablet, 'r', encoding='utf-8')
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
                    SQLfuncs.addYearToTab(buf, tablet)
                    buf = "mu "
                    yearCount += 1
                    continue
                currentLine = tab.readline()
            row += 1
                
