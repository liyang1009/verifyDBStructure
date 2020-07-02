#!/usr/bin/python
# -*- coding: utf-8 -*-
class Table():	
	'''capacity the table declare include indexs/columns/name'''
	def __init__(self,name,statements,indexs):
		self.name = name
		self.indexs = indexs
		self.statements = statements

	def get_statements(self):
		return self.statements

	def get_indexs(self):
		return self.indexs

	def __eq__(self,compared_table):
		pass
class Index():

	def __init__(self,column_name, primary,name):
		self.column_name = column_name
		self.primary = primary
		self.name = name

	def __eq__(self,compared):
		print("call me")
			
class Column():

	def __init__(self,column_name,column_type,column_comment,column_type_len,default_value,column_is_null = True ):
		self.column_name   = column_name
		self.column_type = column_type	
		self.column_comment = column_comment
		self.column_is_null = column_is_null
		self.column_type_len = column_type_len
		self.column_default_value = default_value

	def __eq__(self,other):
		return self.column_name == other.column_name and self.column_type == other.column_type and self.column_is_null == other.column_is_null
			

class token():

	def __init__(self,token_t,token_v,line_no):
		self.token_t = token_t
		self.token_v = token_v
		self.line_no = line_no

class Report():
	def __init__(self):
		self.report_items = []
		self.longest_len = 0

	def add_report(self,item):
		if len(item) > self.longest_len:
			self.longest_len == len(item)
		self.report_items.append(item)
	def display_report(self):
		for item in self.report_items:
			print(item)

