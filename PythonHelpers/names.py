from importlib.resources import path
import os

tablets = os.listdir(".\Translated")

for tablet in tablets:
    output = open("./Names/" + tablet + "names.txt", "w", encoding="utf-8")
    tab = open("./Translated/" + tablet, "r", encoding="utf-8")
    currentLine = tab.readline()
    while currentLine != '':
        test = currentLine.find("\tPN\n")
        if(test != -1):
            output.write(currentLine)
        currentLine = tab.readline()