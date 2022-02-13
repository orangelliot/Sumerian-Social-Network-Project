from fileinput import filename
import openpyxl
import os
from nameGrabber import NameGrabber

tabulatedData = openpyxl.load_workbook(filename = 'tabulatedData.xlsx')

getNames = True
getDates = False

wsNames = tabulatedData.worksheets[0]

if getNames:
    n = NameGrabber(wsNames, os.getcwd() + '/Translated/')
    n.namesToSheet()
    tabulatedData.save('tabulatedData.xlsx')