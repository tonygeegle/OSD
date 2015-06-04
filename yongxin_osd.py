#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.04

from osdlib.yongxin import set_yongxin_osd_request
from osdlib.yongxin import analysis_yongxin_osd_response
import socket
import csv

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

print 'source code file is ' + check_sourcefile_code()
csvfile_code = check_csvfile_code('testcard.csv')
print 'csv file code file is ' + csvfile_code

if __name__=="__main__" and 'GB2312' == csvfile_code:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(("10.230.0.103", 7364))
	with open('testcard.csv','rb') as csv_file:
		next(csv_file)
		csv_reader=csv.reader(csv_file)
		db_id = 1
		for row in csv_reader:
			print len(row[0])
			test = set_yongxin_osd_request(db_id, cardid = row[0], content = row[1], Style = 1, Duration = 10)
			teststr = test.fun_Data_Section()
			#print repr(teststr)
			s.send(teststr)
			teststr_recv = s.recv(1024)
			test_recv = analysis_yongxin_osd_response(yongxin_osd_response = teststr_recv)
			db_id += 1
	s.close()
