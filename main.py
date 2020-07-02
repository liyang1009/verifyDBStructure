#!/usr/bin/python	
# -*- coding: utf-8-*-
'''
this module is for compare the develop environment and production table structure
if equal the deploy is permit otherwise is abort
'''
import pdb
import os
import sys
import argparse
from engine import Engine
'''generate the tokens 
'''
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='verify the dev environment is not equal prod enviornment db table structure')
	parser.add_argument('dev', metavar='-dev', type=str,help='an string for dev db file path')	
	parser.add_argument('prod', metavar='-prod', type=str, help='an string for prod db file path')	
	parser.add_argument('strict',  metavar='-strict', type=bool ,help='is optinal if specify the value is \"-strict\" which can control the column comment is can participate the comare')	
	args = parser.parse_args()
	dev_file = args.dev
	prod_file = args.prod
	strict = args.strict
	engine = Engine(dev_file,prod_file,strict)
	engine.execute()
				
