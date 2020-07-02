#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from parser import Parser
from entity import Report
	
class Engine():

	def __init__(self,from_sqlfile,to_sqlfile,strict = False):
		self.status = True	
		self.report = Report()
		self.strict = strict
		if os.path.isfile(from_sqlfile) and os.path.isfile(to_sqlfile):
			self.from_parser = Parser(from_sqlfile,None)
			self.to_parser = Parser(to_sqlfile,None)
		else:
			self.report.add_report("the file is not exists")
		
	def execute(self):
		'''this is the entry point function scan and parse the sql file generate database structure '''
		dev_database = self.from_parser.parse_tables()	 
		pro_database = self.to_parser.parse_tables()	 
		self._compare(dev_database,pro_database)
		if self.status:
			self.report.add_report("that's fine")
		self.report.display_report()

	def _compare(self,dev_database,pro_database):
		'''compare the database'''
		for name,content in dev_database.items():
			if name not in pro_database:
				self.status = False
				print("the table {1}{0}{2} is not exists ".format(name,"\x1b[6;30;42m","\x1b[0m"))
			else:
				t_table = pro_database[name]
				self.__compare_table(dev_database[name],t_table)

	def _compare_statement(self,col,other,table_name):
		partial = col.column_type == other.column_type and col.column_is_null == other.column_is_null and col.column_type_len == other.column_type_len and col.column_default_value == other.column_default_value
		result = partial and col.column_comment == other.column_comment if self.strict else partial
		if not result:
			self.status = False
			if col.column_type != other.column_type :
				format_str = "the column {0} in table {1} about type is not equal,the dev is {2} and the prod is {3}"
				format_data = [table_name,col.column_name,col.column_type,other.column_type]
				
			elif col.column_type_len != other.column_type_len:
				format_str = "the column {0} in table {1} about type length  is not equal,the dev is {2} and the prod is {3}"
				format_data = [table_name,col.column_name,col.column_type_len,other.column_type_len]

			elif col.column_is_null != other.column_is_null:
				format_str = "this column {2}{1}{3} is not equal about column's not null constraint in table {2}{0}{3}"
				format_data = [table_name,col.column_name,"\x1b[6;30;42m","\x1b[0m"]

			elif col.column_comment != other.column_comment:
				format_str = "this column {2}{1}{4}{3} is not equal about column's comement  in table {2}{0} comment is {5}{3}"
				format_data = [table_name,col.column_name,"\x1b[6;30;42m","\x1b[0m",col.column_comment,other.column_comment]
			else:
				format_str = "this column {2}{1}{4}{3} is not equal about column's default value  in table {2}{0}  is {5}{3}"
				format_data = [table_name,col.column_name,"\x1b[6;30;42m","\x1b[0m",col.column_default_value,other.column_default_value]

			self.report.add_report(format_str.format(*format_data)) 

	def _compare_statements(self,f_table,t_table):
		'''compare the column define'''
		for name,col in f_table["statements"].items():
			if name  in t_table["statements"]  :
				other = t_table["statements"][name]
				self._compare_statement(col,other,f_table["table_name"])
			else:
				self.status = False
				self.report.add_report("this column {2}{1}{3} is not exists in table {2}{0}{3}".format(f_table["table_name"],col.column_name,"\x1b[6;30;42m","\x1b[0m")) 
	
	def _compare_index(self,f_table,t_table):
		'''compare the index define'''
		for name,index in f_table["indexs"].items():
			if name in t_table["indexs"]:
				t_index = t_table["indexs"][name]
				if ",".join(index.column_name) == ",".join(t_index.column_name) and index.primary == t_index.primary and index.name == t_index.name:
					pass
				else:
					self.status = False
					self.report.add_report("the index {2}{0} {3}is not equal in  table {2}{1}{3} " .format(index.name, t_table["table_name"],"\x1b[6;30;42m","\x1b[0m"))
			else:
				self.status = False
				self.report.add_report("the index {2}{0} {3}is not exists in  table {2}{1}{3} " .format(index.name, t_table["table_name"],"\x1b[6;30;42m","\x1b[0m"))

	def __compare_table(self,f_table,t_table):
		'''compare table column and index define'''
		self._compare_statements(f_table,t_table)
		self._compare_index(f_table,t_table)
