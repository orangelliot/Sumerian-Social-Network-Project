import os

rawdata = open("sumerian_untranslated.atf", 'r', encoding="utf-8")

savepathhead = 'Chunks/tablet_chunk_'

currentline = rawdata.readline()
currentTablet = 0
currentChunk = 0
chunkWrite = open(savepathhead + str(currentChunk) + ".atf", 'w', encoding="utf-8")
while currentline != '':
	chunkWrite.write(currentline)
	if currentline == '\n':
		# End of current tablet
		currentTablet += 1
		print("tablet ", currentTablet, ":chunk ", currentChunk, end="\r")
		if currentTablet % 1000 == 0:
			# End of chunk
			currentChunk += 1
			chunkWrite.close()
			chunkWrite = open(savepathhead + str(currentChunk) + ".atf", 'w', encoding="utf-8")
	currentline = rawdata.readline()
