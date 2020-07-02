#!/user/bin/python
# -*- coding: utf-8 -*-
from lexer import Lexer
from entity import *

class Parser():
	'''parser the table definition'''
	def __init__(self,file_path ,content ):
		if content is None:	
			source_text = self._read_file_content(file_path)
		else:
			source_text =content
		self.lexer = Lexer(source_text)
		
	def _read_file_content(self,file_path):
		with open(file_path,"r") as sql_file:
			return sql_file.read()

	def parse_tables(self):
		tables = {}
		while self.lexer.last_token():
			while self.lexer.last_token():
				token = self.lexer.get_keyword()
				if token == "CREATE":
					token_t = self.lexer.get_keyword()
					if token_t == "TABLE":
						break
				
			table_name = self.lexer.get_indentify()
			if not table_name:
				break
			table = {} 
			table["table_name"] = table_name
			table["statements"]= self._parse_statements()
			table["indexs"] = self._parse_indexs()
			tables[table_name] = table
		return tables

	def _parse_statements(self):
		'''construct the column structure list'''
		statements = {}
		while self.lexer.last_token():
			token = self.lexer.next_token()
			if  self.lexer.is_primary_keyword(token):
				break
			column = self._parse_statement()		
			statements[column.column_name] = column
			token = self.lexer.current_token()
		return statements
	
	def _parse_index(self):
		'''parse the single index structure'''
		is_primary = False	
		key_word = self.lexer.get_keyword()	
		index_name = "primary"
		if self.lexer.is_primary_keyword(key_word):
			self.lexer.get_keyword()	
			is_primary = True
		else:
			index_name = self.lexer.get_indentify()	
				
		self.lexer.get_parenthese()
		column_names = []
		while(self.lexer.next_token() != ")"):
			c_name = self.lexer.get_indentify()
			column_names.append(c_name)
			
		self.lexer.get_parenthese()
		index =  Index(column_names,is_primary,index_name)
		return index

	def _parse_indexs(self):
		'''construct the index structure list'''
		indexs = {}
		token = self.lexer.next_token()
		while token != ")":
			index = self._parse_index()
			token = self.lexer.next_token()
			indexs[index.name] = index
		return indexs;
		
	def  _parse_statement(self):
		'''parse the single column structure'''
		column_name = self.lexer.get_indentify()
		column_type = self.lexer.get_keyword()
		state = None
		token = self.lexer.next_token()
		comment = None
		is_null = True
		value = 0
		default_value = None
		while token != ",":
			if token == "(":
				self.lexer.current_token()
				value = self.lexer.current_token()
				self.lexer.get_parenthese()
			elif token == "NOT":
				self._parse_not_null()
				is_null = False

			elif self.lexer.is_default_keyword(token):
				default_value = self._parse_statement_default()

			elif self.lexer.is_comment_keyword(token) :
				comment = self._parse_statement_comment()
			else:
				self.lexer.current_token()	

			token = self.lexer.next_token()

		return Column(column_name,column_type,comment,value,default_value,is_null)

	def _parse_not_null(self):
		self.lexer.get_keyword()
		self.lexer.get_keyword()
		
	def _parse_statement_type_num(self):
		'''parse the variable type length :([0-9]+)'''
		self.lexer.get_parenthese()
		value = self.lexer.get_number()	
		slef.lexer.get_parenthese()
		return value

	def _parse_statement_default(self):
		'''parse the defaule value default :[0-9]+|"\.+"'''
		self.lexer.get_keyword()
		return self.lexer.next_token()

	def _parse_statement_comment(self):
		'''parse column statement :`\.*`'''
		self.lexer.get_keyword()
		comment =  self.lexer.get_comment()
		len_commend = len(comment)
		if comment[0] == "'" and comment[len_commend - 1] == "'":
			return comment
		else:
			token = self.lexer.next_token()
			len_token = len(token)
			partial_tokens = [comment]
			while token[len_token-1] != "'":
				partial_tokens.append(self.lexer.current_token())
				token = self.lexer.next_token()
				len_token = len(token)
			partial_tokens.append(self.lexer.current_token())
			return "".join(partial_tokens) 
