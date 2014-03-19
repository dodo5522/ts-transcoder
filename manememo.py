#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
FILE_INPUT=$1
nkf -w8 ${FILE_INPUT} > ${FILE_INPUT}_1.utf8
sed -e 's/--/0/g' ${FILE_INPUT}_1.utf8 > ${FILE_INPUT}_2.utf8
sed -e '1,6d' ${FILE_INPUT}_2.utf8 > ${FILE_INPUT}_3.utf8
'''

import os,sys,re

_ENCODING = 'utf-8'
_KEY_COMPANY = 'Kigyoumei'

class Record(object):
	'''
	Default record object.
	'''

class RecordOfBank(Record):
	'''
	A record of bank.
	'''

class RecordOfOther(Record):
	'''
	A record of other.
	'''

class RecordOfStock(Record):
	'''
	A record of stock.
	'''

class RecordOfCard(Record):
	'''
	A record of credit card.
	'''

class Table(object):
	'''
	Default table object.
	'''
	
	@classmethod
	def get_kind_table(cls):
		'''Get kind of table.'''
		return ''
	
	@classmethod
	def get_fields(cls):
		'''Get attribute name and value's type as tuple.'''
		return ()
	
	def __init__(self, class_record, lines_csv=None, path_csv_in=None):
		'''
		Constructor of Table class.
		
		Args:
			class_table_record: Record object type to be making from now
			class_record: Class type of record to be stored.
			lines_csv: Lines read from CSV file with unicode.
			path_csv_in: File path of input CSV file.
		'''
		
		self.path_csv_in = path_csv_in
		self.records = []
		self.companies = {}
		
		# make records from each line of CSV data.
		for line in lines_csv:
			obj = class_record()
			values_in_record = line.split(u',')
			
			for i, (field, field_jp, cast) in enumerate(self.get_fields()):
				value = values_in_record[i]
				self._add_value_to_record(obj, field, value, cast)
				
				# to count the number of company to generate output CSV file later.
				if field == _KEY_COMPANY:
					self.companies[value] = None
			
			self.records.append(obj)
	
	def _add_value_to_record(self, obj_record, field, value, cast):
		'''
		Add value which is casted with "cast" to the record object as the attribute with "field".
		Args:
			obj_record: record object
			field: attribute name
			value: string or integer as value
			cast: type to cast the value
		'''
		try:
			casted_value = cast(value)
		except ValueError as err:
			if cast == str:
				casted_value = u''
			else:
				casted_value = 0
		finally:
			setattr(obj_record, field, casted_value)
	
	def write_records_file(self):
		'''Write all record to file.'''
		
		fields = self.get_fields()
		
		# process to devide output CSV file by company name.
		for company in self.companies.keys():
			# generate output CSV file path with company name.
			(path_csv_out, ext) = os.path.splitext(self.path_csv_in)
			path_csv_out += '_' + self.get_kind_table()
			path_csv_out += '_' + company.encode(_ENCODING) + ext
			
			fp = open(path_csv_out, 'w')
			
			for i, (field, field_jp, cast) in enumerate(fields): 
				fp.write(field_jp.encode(_ENCODING))
				if i < len(fields) - 1:
					fp.write(u','.encode(_ENCODING))
				else:
					fp.write(u'\n'.encode(_ENCODING))
			
			for record in self.records:
				# return to the gegining if company name differs from the one of a record.
				value = getattr(record, _KEY_COMPANY)
				if company != value:
					continue
				
				for i, (field, field_jp, cast) in enumerate(fields):
					value = getattr(record, field)
					if type(value) == unicode:
						value = value.encode(_ENCODING)
					else:
						value = str(value)
					fp.write(value)
					if i < len(fields) - 1:
						fp.write(u','.encode(_ENCODING))
					else:
						fp.write(u'\n'.encode(_ENCODING))
			
			fp.close()

class RecordsOfBank(Table):
	'''A table of bank.'''
	
	@classmethod
	def get_kind_table(cls):
		'''Get kind of table.'''
		return 'bank'
	
	@classmethod
	def get_class_record(self):
		'''Get record class.'''
		return RecordOfBank
	
	@classmethod
	def get_fields(cls):
		'''Get attribute name and value's type as tuple.'''
		return (("Gyoukai",u"*業界",unicode),
				(_KEY_COMPANY,u"企業名",unicode),
				("Bikou",u"備考",unicode),
				("Riyoubi",u"ご利用日",unicode),
				("Kubun",u"区分",unicode),
				("Tekiyou",u"摘要",unicode),
				("ShiharaiKingaku_Yen",u"支払金額（円）",int),
				("AzukeireKingaku_Yen",u"預入金額（円）",int),
				("Zandaka_Yen",u"残高（円）",int))

class RecordsOfOther(Table):
	'''A table of other.'''
	
	@classmethod
	def get_kind_table(cls):
		'''Get kind of table.'''
		return 'other'
	
	@classmethod
	def get_class_record(self):
		'''Get record class.'''
		return RecordOfOther
	
	@classmethod
	def get_fields(cls):
		'''Get attribute name and value's type as tuple.'''
		return (("Gyoukai",u"*業界",unicode),
				(_KEY_COMPANY,u"企業名",unicode),
				("Bikou",u"備考",unicode),
				("Riyoubi",u"ご利用日",unicode),
				("Riyousaki",u"ご利用先",unicode),
				("Riyousha",u"ご利用者",unicode),
				("ShiharaiKubun",u"お支払い区分",int),
				("RiyouKingaku_Yen",u"ご利用金額（円）",int),
				("ShiharaiKingaku_Yen",u"お支払い金額（円）",int))

class RecordsOfStock(Table):
	'''A table of stock.'''
	
	@classmethod
	def get_kind_table(cls):
		'''Get kind of table.'''
		return 'stock'
	
	@classmethod
	def get_class_record(self):
		'''Get record class.'''
		return RecordOfStock
	
	@classmethod
	def get_fields(cls):
		'''Get attribute name and value's type as tuple.'''
		return (("Gyoukai",u"*業界",unicode),
				(_KEY_COMPANY,u"企業名",unicode),
				("Bikou",u"備考",unicode),
				("Yakujoubi",u"約定日",unicode),
				("Ukewatashibi",u"受渡日",unicode),
				("Torihikimei",u"取引名",unicode),
				("Meigaramei",u"銘柄名",unicode),
				("Suuryou",u"数量",unicode),
				("Tanka_Yen",u"単価（円）",int),
				("Tsuuka",u"通貨",unicode),
				("UkewatashiDaikin",u"受渡代金（外貨）",unicode),
				("UkewatashiDaikin_Yen",u"受渡代金（円）",int))

class RecordsOfCard(Table):
	'''A table of credit card.'''
	
	@classmethod
	def get_kind_table(cls):
		'''Get kind of table.'''
		return 'card'
	
	@classmethod
	def get_class_record(self):
		'''Get record class.'''
		return RecordOfCard
	
	@classmethod
	def get_fields(cls):
		'''Get attribute name and value's type as tuple.'''
		return (("Gyoukai",u"*業界",unicode),
				(_KEY_COMPANY,u"企業名",unicode),
				("Bikou",u"備考",unicode),
				("Riyoubi",u"ご利用日",unicode),
				("Riyousaki",u"ご利用先",unicode),
				("Riyousha",u"ご利用者",unicode),
				("ShiharaiKubun",u"お支払い区分",int),
				("RiyouKingaku_Yen",u"ご利用金額（円）",int),
				("ShiharaiKingaku_Yen",u"お支払い金額（円）",int))

class Manememo2():
	@classmethod
	def _get_order_tables(cls):
		return (RecordsOfBank,
				RecordsOfOther,
				RecordsOfStock,
				RecordsOfCard)
	
	def __init__(self, path_csv_in=None):
		setattr(self, "path_csv_in", path_csv_in)
	
	def parse(self):
		# get records from the raw CSV file.
		fpin = open(self.path_csv_in)
		for class_table in self._get_order_tables():
			class_record = class_table.get_class_record()
			
			# skip unnecessary lines.
			for line in fpin:
				line_unicode = unicode(line, 'shift-jis').encode(_ENCODING)
				if line_unicode[0] == u'*':
					break
			
			# store the lines needed.
			lines_csv = []
			for line in fpin:
				line_unicode = unicode(line, 'shift-jis').rstrip()
				if len(line_unicode) == 0:
					break
				lines_csv.append(line_unicode)
			
			# store the read data into table object and another CSV file.
			if len(lines_csv) > 0:
				obj = class_table(class_record, lines_csv, self.path_csv_in)
				obj.write_records_file()
		
		fpin.close()







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
		countSection = -1
		
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
					countSection += 1
					
					# skip the first word '*' and store the titles
					self.titleAll[countSection] = stringRawUnicode[1:].split(u',')
				else:
					if boolSectionStart is True:
						# store one line data as list read from CSV file
						listElementOfALine = stringRawUnicode.split(',')
						listTitle = self.titleAll[countSection]
						
						# generate dictionary sorted by title string
						dictElementOfALine = {}
						for title in listTitle:
							indexOfTitle = listTitle.index(title)
							dictElementOfALine.update({title:listElementOfALine[indexOfTitle]})
						
						# store the generated dictionary
						self.dataAll[countSection].append(dictElementOfALine)
			else:
				boolSectionStart = False
		
		fileCsv.close()
		return True

	def getParsedDataAll(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll,self.dataAll)
		else:
			return (None,None)

	def getParsedDataBank(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll[self._indexOfBank],self.dataAll[self._indexOfBank])
		else:
			return (None,None)

	def getParsedDataCard(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll[self._indexOfCard],self.dataAll[self._indexOfCard])
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

	def saveParsedDataBankAsCsv(self,pathCsvFile,titleOfBank=None,dataOfBank=None):
			return self._saveParsedDataToFile(self._indexOfBank,titleOfBank,dataOfBank,pathCsvFile)

	def saveParsedDataCardAsCsv(self,pathCsvFile,titleOfCard=None,dataOfCard=None):
			return self._saveParsedDataToFile(self._indexOfCard,titleOfCard,dataOfCard,pathCsvFile)

	def _saveParsedDataToFile(self,section,titleOfSection,dataOfSection,pathCsvFile):
		# check error
		if not hasattr(self,'titleAll'):
			return False
		if not hasattr(self,'dataAll'):
			return False
		if (titleOfSection is not None and dataOfSection is None) or \
				(titleOfSection is None and dataOfSection is not None):
			return False
		
		# open file with writable if the path is specified.
		fileSaved = open(pathCsvFile,'w')
		
		# generate first line of CSV file
		if titleOfSection is None:
			titleOfSection = self.titleAll[section]
		stringOfLine = titleOfSection[0]
		for title in titleOfSection[1:]:
			stringOfLine = stringOfLine + u',' + title
		stringOfLine = stringOfLine + u'\n'
		
		# write the genareted first line
		fileSaved.write(stringOfLine.encode('utf-8'))
		
		# generate data lines and write them to CSV file
		if dataOfSection is None:
			dataOfSection = self.dataAll[section]
		for data in dataOfSection:
			stringOfLine = data[titleOfSection[0]]
			for title in titleOfSection[1:]:
				stringOfLine = stringOfLine + u',' + data[title]
			stringOfLine = stringOfLine + u'\n'
			fileSaved.write(stringOfLine.encode('utf-8'))
		
		fileSaved.close()
		return True

if __name__ == '__main__':
	
	try:
		pathCsvFile = sys.argv[1]
		
		objManememo = Manememo2(pathCsvFile)
		objManememo.parse()
		
#		objManememo = Manememo()
#		errorCode = objManememo.parseCsvFile(pathCsvFile)
#		(titleAll,dataAll) = objManememo.getParsedDataAll()
#		
#		titleOfBank = titleAll[0]
#		dataOfBank = dataAll[0]
#		keyIn = u'預入金額（円）'
#		keyOut = u'支払金額（円）'
#		keyDiff = u'差額（円）'
#		
#		# dataAll has list of listOfBank, listOfStock, etc.
#		# listOfBank, listOfStock has the list of dictionary data for elements.
#		titleOfBank.append(keyDiff)
#		for dataOfEachLine in dataOfBank:
#			if dataOfEachLine.get(keyOut) == u'--':
#				dataOfEachLine[keyOut] = u'0'
#			if dataOfEachLine.get(keyIn) == u'--':
#				dataOfEachLine[keyIn] = u'0'
#			
#			# Add diff data to each line.
#			intDiff = int(dataOfEachLine.get(keyIn)) - int(dataOfEachLine.get(keyOut))
#			dataOfEachLine[keyDiff] = unicode(str(intDiff))
#		
#		# save bank data in the instance as CSV file
#		pathCsvFileBank = re.sub(r'\.csv$','_bank.csv',pathCsvFile)
#		errorCode = objManememo.saveParsedDataBankAsCsv(pathCsvFileBank,titleOfBank,dataOfBank)
#		
#		titleOfCard = titleAll[3]
#		dataOfCard = dataAll[3]
#		keyOut = u'お支払い金額（円）'
#		
#		# dataAll has list of listOfBank, listOfStock, etc.
#		# listOfBank, listOfStock has the list of dictionary data for elements.
#		for dataOfEachLine in dataOfCard:
#			objectOut = dataOfEachLine.get(keyOut)
#			if objectOut != None and objectOut.isdigit():
#				intOut = int(objectOut) * -1
#				dataOfEachLine[keyOut] = unicode(str(intOut))
#		
#		# save card data in the instance as CSV file
#		pathCsvFileCard = re.sub(r'\.csv$','_card.csv',pathCsvFile)
#		errorCode = objManememo.saveParsedDataCardAsCsv(pathCsvFileCard,titleOfCard,dataOfCard)
	except Exception as err:
		print type(err)
		print err
	finally:
		print "end function."
