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
from yearMatcher import YearMatcher

tabulatedData = openpyxl.load_workbook(filename = 'tabulatedData.xlsx')
yearNames = openpyxl.load_workbook(filename = 'yearNames.xlsx')
wsTabletsNNames = tabulatedData.worksheets[0]
wsTabletsNYears = tabulatedData.worksheets[1]
wsTabletsNYearsBest = tabulatedData.worksheets[2]
wsYearNames = yearNames.worksheets[0]
path = os.getcwd() + '/Translated/'

getNames = True
getYears = False
findBestYears = False

if getNames:
    n = NameGrabber(path)
    n.namesToDB()

if getYears:
    y = YearGrabber(wsTabletsNYears, path)
    y.yearsToSheet()

if findBestYears:
    b = YearMatcher(wsYearNames, wsTabletsNYears, wsTabletsNYearsBest)
    b.bestYearsToSheet()

tabulatedData.save('tabulatedData.xlsx')