# Elliot D Fisk
# Feb 2022
# Program to handle all operations that grab data from raw translated
# tablets and put it into a shared excel spreadsheet

# Usage: add a boolean for each new grabber script and import that script.
#        then pass the desired excel sheet from the tabulatedData workbook
#        object into the grabber. (currently using wsNames, the first sheet)
#        of tabulatedData.xlsx and path, which stores the path where the
#        translated tablet files can be found.

import openpyxl
import os
from nameGrabber import NameGrabber
from yearGrabber import YearGrabber

tabulatedData = openpyxl.load_workbook(filename = 'tabulatedData.xlsx')
wsNames = tabulatedData.worksheets[0]
wsYears = tabulatedData.worksheets[1]
path = os.getcwd() + '/Translated/'

getNames = False
getYears = True

if getNames:
    n = NameGrabber(wsNames, path)
    n.namesToSheet()

if getYears:
    y = YearGrabber(wsYears, path)
    y.yearsToSheet()

    tabulatedData.save('tabulatedData.xlsx')