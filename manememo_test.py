#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
from manememo import Manememo

_pathCsvSrcFile = './btmu_torihiki_20140114004100.csv'
_pathCsvDstFileOfAll = './btmu_torihiki_20140114004100_test_all.csv'
_pathCsvDstFileOfBank = './btmu_torihiki_20140114004100_test_bank.csv'
_pathCsvDstFileOfCard = './btmu_torihiki_20140114004100_test_card.csv'

class TestManememo(unittest.TestCase):
	def test_init(self):
		print "test init start."
		objManememo = Manememo()
		self.assertIsNotNone(objManememo,None)
		self.assertIsInstance(objManememo,Manememo,None)
		print "test init end."
		pass

	def test_parseCsvFile(self):
		print "test parseCsvFile start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		print "test parseCsvFile end."
		pass
		
	def test_getParsedDataAll(self):
		print "test getParsedData start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		print "title data length : %d" % len(titleAll)
		self.assertIsNotNone(dataAll,None)
		print "all data length : %d" % len(dataAll)
		self.assertGreater(len(dataAll),0,None)
		print "bank data length : %d" % len(dataAll[0])
		self.assertGreater(len(dataAll[0]),0,None)
		#print "other data length : %d" % len(dataAll[1])
		#self.assertGreater(len(dataAll[1]),0,None)
		#print "stock data length : %d" % len(dataAll[2])
		#self.assertGreater(len(dataAll[2]),0,None)
		print "credit card length : %d" % len(dataAll[3])
		self.assertGreater(len(dataAll[3]),0,None)
		print "test getParsedData end."
		pass

	def test_getParsedDataBank(self):
		print "test getParsedDataBank start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		
		(titleOfSectionBank,dataOfSectionBank) = objManememo.getParsedDataBank()
		self.assertIsNotNone(titleOfSectionBank,None)
		print "title data length : %d" % len(titleOfSectionBank)
		self.assertIsNotNone(dataOfSectionBank,None)
		print "bank data lines : %d" % len(dataOfSectionBank)
		self.assertGreater(len(dataOfSectionBank),0,None)
		print "each bank data length : %d" % len(dataOfSectionBank[0])
		pass

	def test_getParsedDataCard(self):
		print "test getParsedDataCard start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		
		(titleOfSectionCard,dataOfSectionCard) = objManememo.getParsedDataCard()
		self.assertIsNotNone(titleOfSectionCard,None)
		print "title data length : %d" % len(titleOfSectionCard)
		self.assertIsNotNone(dataOfSectionCard,None)
		print "bank data lines : %d" % len(dataOfSectionCard)
		self.assertGreater(len(dataOfSectionCard),0,None)
		print "each bank data length : %d" % len(dataOfSectionCard[0])
		pass

	def test_setParsedDataAll(self):
		print "test setParsedData start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
		# dataAll has list of listOfBank, listOfStock, etc.
		# listOfBank, listOfStock has the list of dictionary data for elements.
		for data in dataAll:
			for dataOfLine in data:
				if dataOfLine.get(u'支払金額（円）') == u'--':
					dataOfLine[u'支払金額（円）'] = u'0'
				if dataOfLine.get(u'預入金額（円）') == u'--':
					dataOfLine[u'預入金額（円）'] = u'0'
				
				#for key in dataOfLine.keys():
				#	print key.encode('utf-8')+':'+dataOfLine[key].encode('utf-8')
				#print '\n'
		
		# set modified data to instance
		errorCode = objManememo.setParsedDataAll(titleAll,dataAll)
		self.assertTrue(errorCode,None)
		
		# check if the data in the instance does NOT have u'--'
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		
		# dump
		#titleOfBank = titleAll[0]
		#dataOfBank = dataAll[0]
		#for title in titleOfBank:
		#	print title.encode('utf-8')+','
		#for data in dataOfBank:
		#	for title in titleOfBank:
		#		print data[title].encode('utf-8')+','
		
		for data in dataAll:
			for dataOfLine in data:
				self.assertFalse(dataOfLine.get(u'支払金額（円）') == u'--')
				self.assertFalse(dataOfLine.get(u'預入金額（円）') == u'--')
		
		print "test setParsedData end."
		pass

	def test_saveParsedDataAllAsCsv(self):
		print "test saveParsedDataAllAsCsv start."
		objManememo = Manememo()
		
		# should be false if saving all data in the instance to CSV file without requesting parsing
		errorCode = objManememo.saveParsedDataAllAsCsv(_pathCsvDstFileOfAll)
		self.assertFalse(errorCode,None)
		
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
		# save all data in the instance to CSV file
		errorCode = objManememo.saveParsedDataAllAsCsv(_pathCsvDstFileOfAll)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataAllAsCsv end."
		pass

	def test_saveParsedDataBankAsCsv(self):
		print "test saveParsedDataBankAsCsv start."
		objManememo = Manememo()
		
		# should be false if saving all data in the instance to CSV file without requesting parsing
		errorCode = objManememo.saveParsedDataAllAsCsv(_pathCsvDstFileOfBank)
		self.assertFalse(errorCode,None)
		
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
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
		self.assertTrue(errorCode,None)
		
		# save bank data in the instance as CSV file
		errorCode = objManememo.saveParsedDataBankAsCsv(_pathCsvDstFileOfBank)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataBankAsCsv end."
		pass

	def test_saveParsedDataCardAsCsv(self):
		print "test saveParsedDataCardAsCsv start."
		objManememo = Manememo()
		
		# should be false if saving all data in the instance to CSV file without requesting parsing
		errorCode = objManememo.saveParsedDataAllAsCsv(_pathCsvDstFileOfCard)
		self.assertFalse(errorCode,None)
		
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		
		# save card data in the instance as CSV file
		errorCode = objManememo.saveParsedDataCardAsCsv(_pathCsvDstFileOfCard)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataCardAsCsv end."
		pass

if __name__ == '__main__':
	unittest.main()

