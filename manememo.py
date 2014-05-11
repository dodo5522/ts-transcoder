#!/usr/bin/env python2.7
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

class Manememo():
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

if __name__ == '__main__':
	try:
		pathCsvFile = sys.argv[1]
		objManememo = Manememo(pathCsvFile)
		objManememo.parse()
	except Exception as err:
		print type(err)
		print err
	finally:
		print "end function."
