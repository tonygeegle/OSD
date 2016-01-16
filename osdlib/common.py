#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.04

import json

def check_sourcefile_code():
	if "\xd2\xbb" == "一":
		sourcecode = 'GB2312'
	elif "\xe4\xb8\x80" == "一":
		sourcecode = 'UTF8'
	else:
		sourcecode = 'unknown code'
	return sourcecode

def check_csvfile_code(csvfilename):
	csvfilecode = ''
	with open(csvfilename, 'rb') as csv_file:
		firstline = csv_file.readline() # 第一行开头为“智能卡号”四个汉字
		if "\xd6\xc7" == firstline[0:2]: # 要求汉字GB2312编码，因此“智”这个字应该是双字节\xd6\xc7
			csvfilecode = 'GB2312'
		else:
			csvfilecode = 'unknown code'
	return csvfilecode

def get_config(configfilename):
	f = file(configfilename);
	s = json.load(f)
	f.close
	return s
