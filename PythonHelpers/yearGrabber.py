import os
import re

class YearGrabber(object):
    
    def __init__(self, sheet, path):
        self.sheet = sheet
        self.path = path

    def yearsToSheet(self):
        tablets = os.listdir(self.path)
        row = 2
        for tablet in tablets:
            #open each tablet
            tab = open(self.path + tablet, 'r', encoding='utf-8')
            self.sheet['A' + str(row)].value = tablet
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
                    #write buf to excel
                    self.sheet.cell(row, 3 + yearCount).value = buf
                    buf = "mu "
                    yearCount += 1
                    continue
                currentLine = tab.readline()
            self.sheet.cell(row, 2).value = yearCount
            row += 1
                
