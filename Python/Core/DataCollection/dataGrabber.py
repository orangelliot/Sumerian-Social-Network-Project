# Elliot Fisk
# Program to handle all operations that grab data from raw translated
# tablets and put it into a shared excel spreadsheet

# Usage: add a boolean for each new grabber script and import that script.
#        then pass the desired excel sheet from the tabulatedData workbook
#        object into the grabber. (currently using wsNames, the first sheet)
#        of tabulatedData.xlsx and path, which stores the path where the
#        translated tablet files can be found.

import openpyxl
import os
from threadedNameGrabber import ThreadedNameGrabber
from yearGrabber import YearGrabber
from yearMatcher import YearMatcher

#dataVis = openpyxl.load_workbook(filename = 'dataVis.xlsx')
#wsTabLengthVis = dataVis.worksheets[0]

#catalog = openpyxl.load_workbook(filename = 'catalog.xlsx')
#wsYearNamesCat = catalog.worksheets[0]
#wsPlaceNamesCat = catalog.worksheets[1]

path = os.getcwd() + '/Dataset/Translated/'

getNames = True
getYears = False
findBestYears = False

if getNames:
    n = ThreadedNameGrabber(path)
    n.namesToDB()

if getYears:
    y = YearGrabber(path)
    y.yearsToDB()

if findBestYears:
    b = YearMatcher()
    b.bestYearsToSheet()