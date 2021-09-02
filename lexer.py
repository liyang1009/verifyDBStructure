#!/usr/bin/python
# -*- coding: utf-8 -*-
_KEYWORDS = ["DROP",
"CREATE",
"TABLE",
"int",
"char",
"varchar",
"NOT",
"NULL",
"DEFAULT",
"datetime",
"tinyint",
"text",
"PRIMARY",
"KEY",
"AUTO_INCREMENT",
"INDEX",
"COMMENT"]

class Lexer():
	'''scanner for the tokens'''
	def __init__(self,source_text):
		self.source = source_text
		self.pos = -1 
		self._generate_tokens()

	def _generate_tokens(self):
		'''
		consturct the token stack
		'''
		self.source = self.source.replace("\n"," ").replace("\r","").replace("("," ( ").replace(")"," ) ").replace(","," , ")
		self.tokens = self.source.split(" ")
		elements = list() 
		for element in self.tokens:
			if not element:
				continue
			elements.append(element)
			
		self.tokens = elements
		self.tokens_len = len(self.tokens)

	def format_token(self):
		tokens = list() 
		for word in self.tokens:	
			if word in _KEYWORDS:
				t_type = "keyword"
			elif word in ["(",",",")"]:
				t_type = "operator"
			elif "`" in word:
				t_type = "indentify"
			else:
				t_type = "normal"
			tokens.append(token(t_type,word,0))

	def next_token(self):
		'''
		forward the token 
		'''
		if self.last_token():
			return self.tokens[self.pos+1]
	
	def current_token(self):
		'''
		check and consume token from token stack
		'''
		if self.last_token():		
			return self._consume_token()

	def _consume_token(self):
		self.pos = self.pos + 1
		token = self.tokens[self.pos]
		return token

	def get_parenthese(self):
		while self.last_token():
			token = self.next_token()
			if  token in [ "(" ,")",","]:
				return self._consume_token()		

			self._consume_token()

	def get_comment(self):
		'''get commment content'''
		while self.last_token():
			current_token = self.next_token()
			if "'" in current_token:
				return self._consume_token()
			self._consume_token()
	def get_indentify(self):
		while self.last_token():
			current_token = self.next_token()
			if "`" in current_token:
				return self._consume_token()
			self._consume_token()

	def get_keyword(self):
		'''get the keyword token'''
		while self.last_token():
			current_token = self.next_token()
			if current_token in _KEYWORDS:
				return self._consume_token()
			self._consume_token()

	def is_comment_keyword(self,token):
		return token == "COMMENT"

	def is_primary_keyword(self,token):
		return token == "PRIMARY"	

	def is_default_keyword(self,token):
		return token == "DEFAULT"	

	def last_token(self):
		return self.pos != self.tokens_len-1 
		
