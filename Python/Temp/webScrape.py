from errno import EDEADLK
import requests
import time

def getProvenience(TabID):
    URL = "https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&PrimaryPublication=&MuseumNumber=&Provenience=&Period=&TextSearch=&ObjectID=" + TabID +"&requestFrom=Submit"
    page = requests.get(URL)
    startIndex = page.text.index(">Provenience")
    startIndex += len(">Provenience</td><td>")
    endIndex =  page.text.index("</td>" , startIndex , startIndex + 50)

    return page.text[startIndex:endIndex]

def getMassProvenience(TabIDs):
    provList = []
    for TabID in TabIDs:
        time.sleep(.1)
        provList.append(getProvenience(TabID))
    return provList

#ID = ["P142276" , "P102394" , "P118956" , "P102394" , "P109958" , "P115986"]

#print(getMassProvenience(ID))
