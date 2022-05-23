#Elliot Fisk, year matching

import os
from difflib import SequenceMatcher

from Database.SQLfuncs import SQLfuncs

class YearMatcher(object):
    
    def __init__ (self, catalog):
        self.catalog = catalog

    @staticmethod
    def findSimilarityMetric(s1, s2):
        return SequenceMatcher(None, s1, s2).ratio()

    def findMatchingYear(self, yearName):
        bestYear = ''
        row = 1
        similarityMetric = 0
        curYear = self.catalog.cell(row, 1).value
        while curYear != None:
            temp = self.findSimilarityMetric(curYear, yearName)
            if  temp >= similarityMetric:
                similarityMetric = temp
                bestYear = self.catalog.cell(row, 3).value
            row += 1
            curYear = self.catalog.cell(row, 1).value
        return bestYear, similarityMetric

    def bestYearsToDB(self):
        db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
        row = 1
        years = (db.getAttribute("*", "rawyears")[47826:])
        for tuple in years:
            bestSimilarity = 0
            bestYear = 'start'
            year = tuple[0]
            tablet = tuple[1]
            #print("" + year + ", " + tablet + "\n")
            print("%d/%d" % (row, len(years)), end="\r")
            for i in range(self.catalog.cell(1,5).value):
                tempYear, similarity = self.findMatchingYear(year)
                if similarity >= bestSimilarity:
                    bestYear = tempYear
                    bestSimilarity = similarity
            bestSimilarity = bestSimilarity * 10.0
            db.addBestYearToTab(bestYear, tablet, str(int(bestSimilarity)))
            row += 1
            
