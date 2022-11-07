# Length Grabber
# March 2022
# Elliot Fisk
# ---------------
# TODO synopsis and comments v below v
# Elliot Fisk: write data on tablet lengths to excel spreadsheet

import os
import openpyxl

chunks = os.listdir("PythonHelpers/Chunks")
tabulatedData = openpyxl.load_workbook(filename = 'dataVis.xlsx')
hist = tabulatedData.worksheets[3]

row = 1
currentCount = 0
longest = 0

for chunk in chunks:
        cur = open("PythonHelpers/Chunks/" + chunk, 'r', encoding='utf-8')
        currentline = cur.readline()
        while currentline != '':
            if currentline.find("&P") != -1 and currentline[8] == ' ':
                if currentCount != 0:
                    hist['B' + str(row)].value = currentCount
                    if currentCount > longest:
                        longest = currentCount
                row += 1
                hist['A' + str(row)].value = currentline[:8]
                currentCount = 0
            if currentline[0].isnumeric():
                currentCount += 1
            currentline = cur.readline()
hist['C1'].value = row
hist['C2'].value = longest
tabulatedData.save("dataVis.xlsx")