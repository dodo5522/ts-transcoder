#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from manememo import Manememo

_pathCsvSrcFile = './btmu_torihiki_20140114004100.csv'
_pathCsvDstFileOfAll = './btmu_torihiki_20140114004100_all.csv'
_pathCsvDstFileOfBank = './btmu_torihiki_20140114004100_bank.csv'
_pathCsvDstFileOfCard = './btmu_torihiki_20140114004100_card.csv'

class TestManememo(unittest.TestCase):
	def test_init(self):
		print "test init start."
		_objManememo = Manememo()
		self.assertIsNotNone(_objManememo,None)
		self.assertIsInstance(_objManememo,Manememo,None)
		print "test init end."
		pass

	def test_parseCsvFile(self):
		print "test parseCsvFile start."
		_objManememo = Manememo()
		_errorCode = _objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(_errorCode,None)
		print "test parseCsvFile end."
		pass
		
	def test_getParsedDataAll(self):
		print "test getParsedData start."
		_objManememo = Manememo()
		_errorCode = _objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(_errorCode,None)
		
		(titleAll,dataAll) = _objManememo.getParsedDataAll()
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

	def test_saveParsedDataAllAsCsv(self):
		print "test saveParsedDataAllAsCsv start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
		errorCode = objManememo.saveParsedDataAllAsCsv(titleAll,dataAll,_pathCsvDstFileOfAll)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataAllAsCsv end."
		pass

	def test_saveParsedDataBankAsCsv(self):
		print "test saveParsedDataBankAsCsv start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
		# index 0 means Bank data
		titleOfBank = titleAll[0]	
		self.assertGreater(len(titleOfBank),0,None)
		dataOfBank = dataAll[0]
		self.assertGreater(len(dataOfBank),0,None)
		
		errorCode = objManememo.saveParsedDataBankAsCsv(titleOfBank,dataOfBank,_pathCsvDstFileOfBank)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataBankAsCsv end."
		pass

	def test_saveParsedDataCardAsCsv(self):
		print "test saveParsedDataCardAsCsv start."
		objManememo = Manememo()
		errorCode = objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(errorCode,None)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		self.assertIsNotNone(titleAll,None)
		self.assertIsNotNone(dataAll,None)
		
		# index 3 means Credit Card data
		titleOfCard = titleAll[3]	
		self.assertGreater(len(titleOfCard),0,None)
		dataOfCard = dataAll[3]
		self.assertGreater(len(dataOfCard),0,None)
		
		errorCode = objManememo.saveParsedDataCardAsCsv(titleOfCard,dataOfCard,_pathCsvDstFileOfCard)
		self.assertTrue(errorCode,None)
		print "test saveParsedDataCardAsCsv end."
		pass

if __name__ == '__main__':
	unittest.main()

