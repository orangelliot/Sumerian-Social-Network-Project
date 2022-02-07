from importlib.resources import path
import os

tablets = os.listdir("../Translated")

fileCount = len(tablets)
currentCount = 0

for tablet in tablets:
    currentCount = currentCount + 1
    print(str(currentCount) + "/" + str(fileCount), end="\r")
    # Open tablet and new output file
    output = open("../Names/" + tablet + "names.txt", "w", encoding="utf-8")
    tab = open("../Translated/" + tablet, "r", encoding="utf-8")

    # Arrays to hold usefull information
    names = []
    months = []
    years = []
    celestials = []

    # Start reading the tablet
    currentLine = tab.readline()

    # write tablet name to output file
    output.write(currentLine[-8:])

    while currentLine != '':
        # Tokenize the line and grab the name
        tokenLine = currentLine.split('\t')

        # Found Personal Name
        if(currentLine.find("\tPN\n") != -1):
            names.append(tokenLine[1])

        # Found month name
        if(currentLine.find("\tMN\n") != -1):
            months.append(tokenLine[1])

        # Found year name
        if(currentLine.find("\tYN\n") != -1):
            years.append(tokenLine[1])

        # Found celestial name
        if(currentLine.find("\tCN\n") != -1):
            celestials.append(tokenLine[1])

        # Continue reading the tablet
        currentLine = tab.readline()
    
    # write output
    # Names
    if len(names) == 0:
        output.write("NONE\n")
    else:
        for name in names:
            output.write(name + "\n")
    output.write("\n")
    # Months
    if len(months) == 0:
        output.write("NONE\n")
    else:
        for month in months:
            output.write(month + "\n")
    output.write("\n")
    # Years
    if len(years) == 0:
        output.write("NONE\n")
    else:
        for year in years:
            output.write(year + "\n")
    output.write("\n")
    # Celestials
    if len(celestials) == 0:
        output.write("NONE\n")
    else:
        for celestial in celestials:
            output.write(celestial + "\n")
    output.write("\n")
# print again so the progress text is not lost
print(str(currentCount) + "/" + str(fileCount))