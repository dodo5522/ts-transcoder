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
		print "parseCsvFile"
		return True

	def getParsedData(self,dataAll):
		print "getParsedData"
		return True

if __name__ == '__main__':
	mm = Manememo()

