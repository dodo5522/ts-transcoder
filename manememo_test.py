#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from manememo import Manememo

_pathCsvSrcFile = './btmu_torihiki_20140114004100.csv'

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
		
	def test_getParsedData(self):
		print "test getParsedData start."
		_objManememo = Manememo()
		_errorCode = _objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(_errorCode,None)
		
		dataAll = _objManememo.getParsedData()
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

if __name__ == '__main__':
	unittest.main()

