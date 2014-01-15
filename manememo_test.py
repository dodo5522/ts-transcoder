#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from manememo import Manememo

_pathCsvSrcFile = './btmu_torihiki_20140114004100.csv'

class TestManememo(unittest.TestCase):
	def test_init(self):
		_objManememo = Manememo()
		self.assertIsNotNone(_objManememo,None)
		self.assertIsInstance(_objManememo,Manememo,None)
		pass

	def test_parseCsvFile(self):
		_objManememo = Manememo()
		_errorCode = _objManememo.parseCsvFile(_pathCsvSrcFile)
		self.assertTrue(_errorCode,None)
		pass
		
	def test_getParsedData(self):
		_objManememo = Manememo()
		_dataOfBank = []
		_dataOfOther = []
		_dataOfStock = []
		_dataOfCard = []
		_dataAll = [_dataOfBank,_dataOfOther,_dataOfStock,_dataOfCard]
		
		_errorCode = _objManememo.getParsedData(_dataAll)
		self.assertTrue(_errorCode,None)
		self.assertGreaterEqual(_dataAll[0],0,None)
		self.assertGreaterEqual(_dataAll[1],0,None)
		self.assertGreaterEqual(_dataAll[2],0,None)
		self.assertGreaterEqual(_dataAll[3],0,None)
		pass

if __name__ == '__main__':
	unittest.main()

