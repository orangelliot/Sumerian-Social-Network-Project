#Elliot Fisk, year matching

import os
from difflib import SequenceMatcher

class YearMatcher(object):
    
    def __init__ (self, yearNames, tabletsNYears, tabletsNYearsBest):
        self.yearNames = yearNames
        self.tabletsNYears = tabletsNYears
        self.tabletsNYearsBest = tabletsNYearsBest

    @staticmethod
    def findSimilarityMetric(s1, s2):
        return SequenceMatcher(None, s1, s2).ratio()

    def findMatchingYear(self, yearName):
        bestYear = ''
        row = 1
        similarityMetric = 0
        curYear = self.yearNames.cell(row, 1).value
        while curYear != None:
            temp = self.findSimilarityMetric(curYear, yearName)
            if  temp >= similarityMetric:
                similarityMetric = temp
                bestYear = self.yearNames.cell(row, 3).value
            row += 1
            curYear = self.yearNames.cell(row, 1).value
        return bestYear, similarityMetric


    def bestYearsToSheet(self):
        row = 2
        tablet = self.tabletsNYears.cell(row, 1).value
        while tablet != None:
            numYears = int(self.tabletsNYears.cell(row, 2).value)
            bestSimilarity = 0
            bestYear = 'start'
            for x in range(numYears):
                year, similarity = self.findMatchingYear(self.tabletsNYears.cell(row, 3 + x).value)
                if similarity >= bestSimilarity:
                    bestYear = year
                    bestSimilarity = similarity
            self.tabletsNYearsBest.cell(row, 1).value = tablet
            self.tabletsNYearsBest.cell(row, 2).value = bestYear
            self.tabletsNYearsBest.cell(row, 3).value = bestSimilarity
            row += 1
            tablet = self.tabletsNYears.cell(row, 1).value
            
