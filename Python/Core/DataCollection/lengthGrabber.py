import os
import openpyxl

<<<<<<< HEAD
=======
chunks = os.listdir("PythonHelpers/Chunks")
>>>>>>> 0d6286bb0abd9ac8555b89306a4908939bbcddd9
tabulatedData = openpyxl.load_workbook(filename = 'tabulatedData.xlsx')
hist = tabulatedData.worksheets[3]

row = 1
currentCount = 0
longest = 0

<<<<<<< HEAD
cur = open("PythonHelpers/Untranslated/ur3_untranslated.atf", 'r', encoding='utf-8')
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
=======
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
>>>>>>> 0d6286bb0abd9ac8555b89306a4908939bbcddd9
hist['C1'].value = row
hist['C2'].value = longest
tabulatedData.save("tabulatedData.xlsx")