#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
FILE_INPUT=$1
nkf -w8 ${FILE_INPUT} > ${FILE_INPUT}_1.utf8
sed -e 's/--/0/g' ${FILE_INPUT}_1.utf8 > ${FILE_INPUT}_2.utf8
sed -e '1,6d' ${FILE_INPUT}_2.utf8 > ${FILE_INPUT}_3.utf8
'''

class Manememo:
	def __init__(self):
		print "constructor is called."

	def __del__(self):
		print "destructor is called."

	def parseCsvFile(self,pathCsvFile):
		titleOfBank = []
		titleOfOther = []
		titleOfStock = []
		titleOfCard = []
		titleAll = [titleOfBank,titleOfOther,titleOfStock,titleOfCard]
		
		listDataOfBank = []
		listDataOfOther = []
		listDataOfStock = []
		listDataOfCard = []
		dataAll = [listDataOfBank,listDataOfOther,listDataOfStock,listDataOfCard]
		
		boolSectionStart = False
		fileCsv = open(pathCsvFile)
		
		# count to array titleOfAll and dataAll
		countListAll = -1
		
		# read csv file and store the data into internal buffer
		for line in fileCsv:
			# translate to unicode and delete line feed code
			stringRawUnicode = unicode(line,'shift-jis').rstrip()
			stringRawUtf8 = stringRawUnicode.encode('utf-8')
			
			# skip blank lines
			if len(stringRawUnicode) > 0:
				# section starts with '*'
				if boolSectionStart is False and stringRawUtf8[0] is '*':
					boolSectionStart = True
					countListAll += 1
					
					# skip the first word '*' and store the titles
					titleAll[countListAll] = stringRawUnicode[1:].split(u',')
				else:
					if boolSectionStart is True:
						# store one line data as list read from CSV file
						listElementOfALine = stringRawUnicode.split(',')
						listTitle = titleAll[countListAll]
						
						# generate dictionary sorted by title string
						dictElementOfALine = {}
						for title in listTitle:
							indexOfTitle = listTitle.index(title)
							dictElementOfALine.update({title:listElementOfALine[indexOfTitle]})
						
						# store the generated dictionary
						dataAll[countListAll].append(dictElementOfALine)
			else:
				boolSectionStart = False
		
		fileCsv.close()
		return True

	def getParsedData(self,dataAll):
		print "getParsedData"
		return True

if __name__ == '__main__':
	mm = Manememo()

