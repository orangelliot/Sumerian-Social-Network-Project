# Elliot Fisk
# Feb 2022
# Program to get names from tablets in self.path and print them
# into self.sheet

# Usage: Import to grabber and create new object with sheet and path
#        then run namesToSheet.

import os
from SQLfuncs import SQLfuncs

class NameGrabber(object):
    
    def __init__(self, path):
        self.path = path

    def namesToDB(self):
        db = SQLfuncs('localhost', 'elliot', 'password')
        tablets = os.listdir(self.path)
        for tabid in tablets:
            #open each tablet
            tab = open(self.path + tabid, 'r', encoding='utf-8')
            #track number of names
            nameCount = 0
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
                        db.addNameToTab(tokenLine[1], tabid)
                        nameCount += 1
                currentLine = tab.readline()
