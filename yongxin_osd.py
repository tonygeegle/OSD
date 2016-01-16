#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.04

from osdlib import *
import socket
import csv
import os

print 'source code file is ' + check_sourcefile_code()
csvfile_code = check_csvfile_code('yongxincard.csv')
print 'csv file is ' + csvfile_code

config_json = get_config("config.json")

if __name__=="__main__" and 'GB2312' == csvfile_code:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((config_json["yognxin"]["ip"], config_json["yongxin"]["port"]))
	with open('yongxincard.csv','rb') as csv_file:
		next(csv_file)
		csv_reader=csv.reader(csv_file)
		db_id = 1
		for row in csv_reader:
			test = set_yongxin_osd_request(db_id, cardid = row[0], content = row[1], Style = config_json["yognxin"]["Style"], Duration = config_json["yognxin"]["Duration"])
			teststr = test.set_Data_Section()
			#print repr(teststr)
			try:
				s.send(teststr)
				print str(db_id) + "\t" + str(row[0]) + "\tSent OK"
			except Exception, ex:
				print str(db_id) + "\t" + str(row[0]) + "\tSent Error: " + str(ex)
			try:
				teststr_recv = s.recv(10240)
				test_recv = analysis_yongxin_osd_response(yongxin_osd_response = teststr_recv)
				test_errocode = test_recv.get_errocode_from_content()
				print repr(test_recv.DB_ID) + "\t" + str(test_errocode.decode("utf8").encode("GB2312")) + "\n"
			except Exception, ex:
				print "xxoo........................."
			db_id += 1
	s.close()

os.system("pause")
