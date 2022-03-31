import os

rawdata = open("sumerian_untranslated.atf", 'r', encoding="utf-8")

currentline = rawdata.readline()
tabletCount = 0
while currentline != '':
	if currentline.find('&P') != -1 and currentline[8] == ' ':
		tabletCount += 1
	currentline = rawdata.readline()

print(tabletCount)
