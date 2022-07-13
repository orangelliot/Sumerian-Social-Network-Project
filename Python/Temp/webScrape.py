from errno import EDEADLK
import requests
import time
import os

def getProvenience(TabID):
    URL = "https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&PrimaryPublication=&MuseumNumber=&Provenience=&Period=&TextSearch=&ObjectID=" + TabID +"&requestFrom=Submit"
    page = requests.get(URL)

    try:
        startIndex = page.text.index(">Provenience")
        startIndex += len(">Provenience</td><td>")
        endIndex =  page.text.index("</td>" , startIndex , startIndex + 50)
    except:
        return "..."

    return page.text[startIndex:endIndex]

def getMassProvenience():
    path = os.getcwd()
    path = path[:len(path) - 11]
    path = path + 'Dataset/Translated/'

    tablets = os.listdir(path)

    file = open("../../Dataset/Output/provenience.csv", "w")
    file.write("TabID,Provenience\n")

    for tablet in tablets:
        tabid = tablet[:7]
        time.sleep(.001)
        prov = getProvenience(tabid)
        file.write(tabid + "," + prov + "\n")

    file.close()

def getSubMassProvenience():
    path = os.getcwd()
    path = path[:len(path) - 11]
    path = path + 'Dataset/Translated/'

    tablets = os.listdir(path)

    file = open("../../Dataset/Output/provenience_1.csv", "w")
    file.write("TabID,Provenience\n")

    condition = "false"

    for tablet in tablets:
        tabid = tablet[:7]

        if tabid == "P121703":
            condition = "true"
        if tabid == "P340164":
            condition = "false"

        if condition == "true":
            time.sleep(.001)
            prov = getProvenience(tabid)
            file.write(tabid + "," + prov + "\n")

    file.close()

#getMassProvenience()
getSubMassProvenience()
