#-*- encoding: utf-8 -*-
import json
import socket
import sys
import time
import struct
import hashlib
import binascii
import csv

class set_yongxin_osd_request(object):
	def __init__(self, db_id = 1, cardid = '8537003845028690', content = "1010测试1010", Style = 1, Duration = 10):
		self.db_id = db_id
		self.cardid = cardid
		self.content = content
		self.Style = Style
		self.Duration = Duration

	def fun_Data_Cont(self):
		Exp_Char = "card=" + self.cardid
		Exp_Len = struct.pack('>B',len(Exp_Char))
		Cont_Char = self.content
		Cont_Len = struct.pack('>B',len(Cont_Char))
		Style = struct.pack('>B', self.Style)
		Duration = struct.pack('>L', self.Duration)
		return Exp_Len + Exp_Char + Cont_Len + Cont_Char + Style + Duration

	def fun_Data_Body(self):
		DB_ID = struct.pack('>H', self.db_id)
		Msg_ID = "\x03\x04"
		Data_Cont = self.fun_Data_Cont()
		Data_Len = struct.pack('>H',len(Data_Cont))
		bytes_need_to_padding = 8 - len(DB_ID + Msg_ID + Data_Cont + Data_Len)%8
		Padding_Byte = ""
		for i in range(bytes_need_to_padding):
			Padding_Byte += "\x00"
		MAC = binascii.a2b_hex(hashlib.md5(DB_ID + Msg_ID + Data_Len + Data_Cont + Padding_Byte).hexdigest())
		return DB_ID + Msg_ID + Data_Len + Data_Cont + Padding_Byte + MAC

	def fun_Data_Section(self):
		Proto_Ver = "\x01"
		Crypt_Ver_and_Key_Type = "\x06"
		OPE_ID = "\xff\xff"
		SMS_ID = "\x00\x01"
		Data_Body = self.fun_Data_Body()
		DB_Len = struct.pack('>H',len(Data_Body))
		return Proto_Ver + Crypt_Ver_and_Key_Type + OPE_ID + SMS_ID + DB_Len + Data_Body

class analysis_yongxin_osd_response(object):
	def __init__(self, yongxin_osd_response = "\x01\x06\xff\xff\x00\x01\x00\x1a\x00\x01\x83\x04\x00\x04\x00\x00\x00\x00\xd7\x36\xf5\x8d\x92\x58\x69\x70\xc0\xa3\x38\x21\x85\x5b\x36\x8d"):
		self.yongxin_osd_response = yongxin_osd_response
		self.Proto_Ver = self.yongxin_osd_response[0:1]
		self.Crypt_Ver_and_Key_Type = self.yongxin_osd_response[1:2]
		self.OPE_ID = self.yongxin_osd_response[2:4]
		self.SMS_ID = self.yongxin_osd_response[4:6]
		self.DB_Len = self.yongxin_osd_response[6:8]
		self.Data_Body = self.yongxin_osd_response[8:]
		if len(self.Data_Body) == struct.unpack('>H',self.DB_Len)[0]: # 判断长度是否正常
			print "len right"
		else:
			print "len error"
		self.MAC = self.Data_Body[-16:]
		if binascii.a2b_hex(hashlib.md5(self.Data_Body[:-16]).hexdigest()) == self.MAC: # 判断MD5校验是否通过
			print "hash right"
		else:
			print "hash wrong"
		self.DB_ID = self.Data_Body[0:2]
		print repr(self.DB_ID)
		self.Msg_ID = self.Data_Body[2:4]
		print repr(self.Msg_ID)
		self.Data_Len = self.Data_Body[4:6]
		print repr(self.Data_Len)
		self.Erro_Code = self.Data_Body[6:10]
		print repr(self.Erro_Code)

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
			test = set_yongxin_osd_request(db_id, cardid = row[0], content = row[1], Style = 1, Duration = 10)
			teststr = test.fun_Data_Section()
			#print repr(teststr)
			s.send(teststr)
			teststr_recv = s.recv(1024)
			test_recv = analysis_yongxin_osd_response(yongxin_osd_response = teststr_recv)
			db_id += 1
	s.close()
