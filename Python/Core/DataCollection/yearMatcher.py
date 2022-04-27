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
        years = db.getAttribute('rawyears', '*')
        for tuple in years:
            numYears = int(self.catalog.cell(row, 5).value)
            bestSimilarity = 0
            bestYear = 'start'
            tablet = tuple[0]
            year = tuple[1]
            for i in range(numYears):
                year, similarity = self.findMatchingYear(year)
                if similarity >= bestSimilarity:
                    bestYear = year
                    bestSimilarity = similarity
            db.addBestYearToTab(bestYear, tablet, bestSimilarity)
            row += 1
            
