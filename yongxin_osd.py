#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.04

from osdlib import *
import socket
import csv

print 'source code file is ' + check_sourcefile_code()
csvfile_code = check_csvfile_code('testcard.csv')
print 'csv file is ' + csvfile_code

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
			teststr = test.set_Data_Section()
			#print repr(teststr)
			s.send(teststr)
			teststr_recv = s.recv(1024)
			test_recv = analysis_yongxin_osd_response(yongxin_osd_response = teststr_recv)
			db_id += 1
	s.close()

