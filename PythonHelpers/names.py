from importlib.resources import path
import os

tablets = os.listdir(".\Translated")

for tablet in tablets:
    output = open("./Names/" + tablet + "names.txt", "w", encoding="utf-8")
    tab = open("./Translated/" + tablet, "r", encoding="utf-8")
    place = False
    currentLine = tab.readline()
    while currentLine != '':
        if(currentLine.find("\tPN\n") != -1 and place == False):
            output.write(currentLine)
        if(currentLine.find("[place]") != -1):
            place = True
        else:
            place = False
        currentLine = tab.readline()