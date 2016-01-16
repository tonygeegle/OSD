#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.13

from osdlib import *
import socket
import csv
import os
import time
import threading

print 'source code file is ' + check_sourcefile_code()
csvfile_code = check_csvfile_code('shumacard.csv')
print 'csv file is ' + csvfile_code

config_json = get_config("config.json")

class SHUMA_OSD_TCP_Thread(threading.Thread): # 每个线程，一个TCP连接
	def __init__(self, threadid, config_json):
		threading.Thread.__init__(self)
		self.threadid = int(threadid)
		self.ip = config_json["shuma"]["ip"]
		self.port = config_json["shuma"]["port"]

	def run(self):
		global mylock, all_content
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((self.ip, self.port))
		SessionID = self.threadid
		while True:
			mylock.acquire()
			try:
				row = all_content.pop()
				mylock.release()
				test = set_shuma_osd_request(SessionID, Card_ID = row[0], Data_content = row[1], Show_Times = config_json["shuma"]["Show_Times"], Expired_Time = int(time.time()+3600))
				teststr = test.set_Data_Section()
				try:
					s.send(teststr)
					print str(SessionID) + "\t" + str(row[0]) + "\tSent OK\n"
				except Exception, ex:
					print str(SessionID) + "\t" + str(row[0]) + "\tSent Error: " + str(ex) + "\n"
				try:
					teststr_recv = s.recv(10240)
					test_recv = analysis_shuma_osd_response(shuma_osd_response = teststr_recv)
					test_errocode = test_recv.get_errocode_from_content()
					print repr(test_recv.SessionID) + "\t" + str(test_errocode.decode("utf8").encode("GB2312")) + "\n"
				except Exception, ex:
					print ex
					print "xxoo.........................\n"
				SessionID += 50
			except Exception, ex:
				mylock.release()
				s.close()
				return "文件全部读取完成"
		s.close()

if __name__ == "__main__" and 'GB2312' == csvfile_code:
	print time.time()
	all_content = []
	mylock = threading.Lock() # 创建锁
	threads = [] # 保存线程列表

	with open('shumacard.csv','rb') as csv_file:
		next(csv_file)
		csv_reader=csv.reader(csv_file)
		for row in csv_reader:
			all_content.append(row)

	for i in range(1,51): # 创建线程对象，每个SMS和CAS之间可以建立50个TCP连接
		threads.append(SHUMA_OSD_TCP_Thread(i))
	for t in threads: # 启动线程
		t.start()
		time.sleep(0.02)
	for t in threads: # 这时上面的线程全部启动了，等待所有线程都结束
		t.join()

	print time.time()
	os.system("pause")
