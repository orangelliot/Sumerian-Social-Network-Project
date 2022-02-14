# Elliot Fisk
# Feb 2022
# Program to get names from tablets in self.path and print them
# into self.sheet

# Usage: Import to grabber and create new object with sheet and path
#        then run namesToSheet.

import os

class NameGrabber(object):
    
    def __init__(self, sheet, path):
            self.sheet = sheet
            self.path = path

    def namesToSheet(self):
        tablets = os.listdir(os.getcwd() + '/Translated')
        row = 2
        for tablet in tablets:
            #open each tablet
            tab = open(self.path + tablet, 'r', encoding='utf-8')
            #track number of names
            nameCount = 0
            #name the row after the tablet it contains
            self.sheet['A' + str(row)].value = tablet
            #start read
            currentline = tab.readline()
            placeName = False
            #continue until end of tablet
            while currentline != '':
                #split line around tab and tokenize
                tokenline = currentline.split('\t')
                if(currentline.find("[place]") != -1):
                    placeName = True
                if(currentline.find("\tPN\n") != -1):
                    if(placeName):
                        #catch placeNames and dont add them to the spreadsheet
                        placeName = False
                    else:
                        #if PN then add to spreadsheet
                        self.sheet.cell(row, 3 + nameCount).value = tokenline[1]
                        nameCount += 1
                currentline = tab.readline()
            self.sheet.cell(row, 2).value = nameCount
            #increment to next line of spreadsheet
            row += 1
