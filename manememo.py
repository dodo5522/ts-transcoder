#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
FILE_INPUT=$1
nkf -w8 ${FILE_INPUT} > ${FILE_INPUT}_1.utf8
sed -e 's/--/0/g' ${FILE_INPUT}_1.utf8 > ${FILE_INPUT}_2.utf8
sed -e '1,6d' ${FILE_INPUT}_2.utf8 > ${FILE_INPUT}_3.utf8
'''

import sys

class Manememo:
	_indexOfBank = 0
	_indexOfOther = 1
	_indexOfStock = 2
	_indexOfCard = 3

	def __init__(self):
		return

	def __del__(self):
		return

	def parseCsvFile(self,pathCsvFile):
		self.titleOfBank = []
		self.titleOfOther = []
		self.titleOfStock = []
		self.titleOfCard = []
		self.titleAll = [self.titleOfBank,self.titleOfOther,self.titleOfStock,self.titleOfCard]
		
		self.listDataOfBank = []
		self.listDataOfOther = []
		self.listDataOfStock = []
		self.listDataOfCard = []
		self.dataAll = [self.listDataOfBank,self.listDataOfOther,self.listDataOfStock,self.listDataOfCard]
		
		boolSectionStart = False
		fileCsv = open(pathCsvFile)
		
		# count to array self.titleOfAll and self.dataAll
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
					self.titleAll[countListAll] = stringRawUnicode[1:].split(u',')
				else:
					if boolSectionStart is True:
						# store one line data as list read from CSV file
						listElementOfALine = stringRawUnicode.split(',')
						listTitle = self.titleAll[countListAll]
						
						# generate dictionary sorted by title string
						dictElementOfALine = {}
						for title in listTitle:
							indexOfTitle = listTitle.index(title)
							dictElementOfALine.update({title:listElementOfALine[indexOfTitle]})
						
						# store the generated dictionary
						self.dataAll[countListAll].append(dictElementOfALine)
			else:
				boolSectionStart = False
		
		fileCsv.close()
		return True

	def getParsedDataAll(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll,self.dataAll)
		else:
			return (None,None)

	def setParsedDataAll(self,titleAll,dataAll):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			self.titleAll = titleAll
			self.dataAll = dataAll
			return True
		else:
			return False

	def saveParsedDataAllAsCsv(self,pathCsvFile):
		# check error
		if not hasattr(self,'titleAll'):
			return False
		if not hasattr(self,'dataAll'):
			return False
		
		# FIXME:
		return True

	def saveParsedDataBankAsCsv(self,pathCsvFile):
		return self._saveParsedDataToFile(self._indexOfBank,pathCsvFile)

	def saveParsedDataCardAsCsv(self,pathCsvFile):
		return self._saveParsedDataToFile(self._indexOfCard,pathCsvFile)

	def _saveParsedDataToFile(self,index,pathCsvFile):
		# check error
		if not hasattr(self,'titleAll'):
			return False
		if not hasattr(self,'dataAll'):
			return False
		
		# open file with writable if the path is specified.
		fileSaved = open(pathCsvFile,'w')
		
		# generate first line of CSV file
		titleOfBank = self.titleAll[index]
		stringOfLine = titleOfBank[0]
		for title in titleOfBank[1:]:
			stringOfLine = stringOfLine + u',' + title
		stringOfLine = stringOfLine + u'\n'
		
		# write the genareted first line
		fileSaved.write(stringOfLine.encode('utf-8'))
		
		# generate data lines and write them to CSV file
		dataOfBank = self.dataAll[index]
		for data in dataOfBank:
			stringOfLine = data[titleOfBank[0]]
			for title in titleOfBank[1:]:
				stringOfLine = stringOfLine + u',' + data[title]
			stringOfLine = stringOfLine + u'\n'
			fileSaved.write(stringOfLine.encode('utf-8'))
		
		fileSaved.close()
		return True

if __name__ == '__main__':
	try:
		pathCsvFile = sys.argv[1]
		objManememo = Manememo()
		
		errorCode = objManememo.parseCsvFile(pathCsvFile)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		
		# dataAll has list of listOfBank, listOfStock, etc.
		# listOfBank, listOfStock has the list of dictionary data for elements.
		for data in dataAll:
			for dataOfLine in data:
				if dataOfLine.get(u'支払金額（円）') == u'--':
					dataOfLine[u'支払金額（円）'] = u'0'
				if dataOfLine.get(u'預入金額（円）') == u'--':
					dataOfLine[u'預入金額（円）'] = u'0'
		
		# set modified data to instance
		errorCode = objManememo.setParsedDataAll(titleAll,dataAll)
		
		# save bank data in the instance as CSV file
		errorCode = objManememo.saveParsedDataBankAsCsv(pathCsvFile+'_bank')
		
		# save card data in the instance as CSV file
		errorCode = objManememo.saveParsedDataCardAsCsv(pathCsvFile+'_card')
	except Exception as err:
		print err
	finally:
		print "end function."
