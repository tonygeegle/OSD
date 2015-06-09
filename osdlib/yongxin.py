#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.04
import struct
import hashlib
import binascii
import re

class set_yongxin_osd_request(object):
	"""
	Data_Section
	  |--Proto_Ver
	  |--Crypt_Ver
	  |--Key_Type
	  |--OPE_ID
	  |--SMS_ID
	  |--DB_Len
	  |--Data_Body
	      |--DB_ID
	      |--Msg_ID
	      |--Data_Len
	      |--Data_Cont
	          |--Exp_Len
	          |--Exp_Char
	          |--Cont_Len
	          |--Cont_Char
	          |--Style
	          |--Duration
	      |--Padding_Byte
	      |--MAC
	"""
	def __init__(self, db_id = 1, cardid = '8537003845028690', content = "1010测试1010", Style = 1, Duration = 10):
		self.db_id = int(re.findall(r"\d+",str(db_id))[0])
		self.cardid = str(re.findall(r"8\d{15}",str(cardid))[0]) # 确保是以8开头的16位智能卡号
		self.content = str(content)
		self.Style = int(Style)
		self.Duration = int(Duration)
		re.purge()

	def set_Data_Content(self):
		Exp_Char = "card=" + self.cardid
		Exp_Len = struct.pack('>B',len(Exp_Char)) # 1字节16进制，无符号字符型，大端网络序
		Cont_Char = self.content
		Cont_Len = struct.pack('>B',len(Cont_Char))
		Style = struct.pack('>B', self.Style)
		Duration = struct.pack('>L', self.Duration) # 4字节16进制，无符号长整型，大端网络序
		return Exp_Len + Exp_Char + Cont_Len + Cont_Char + Style + Duration

	def set_Data_Body(self):
		DB_ID = struct.pack('>H', self.db_id) # 2字节16进制，无符号短整形，大端网络序
		Msg_ID = "\x03\x04" # OSD功能的代码
		Data_Cont = self.set_Data_Content()
		Data_Len = struct.pack('>H',len(Data_Cont))
		bytes_need_to_padding = 8 - len(DB_ID + Msg_ID + Data_Cont + Data_Len)%8 # 不足8倍数个字节，要补足，以便加密
		# 如果数据长度是8的倍数，没必要补全字节，但8减去len%8为8，会多加八个字节，占用网络资源
		bytes_need_to_padding = 0 if 8 == bytes_need_to_padding else bytes_need_to_padding
		Padding_Byte = ""
		for i in range(bytes_need_to_padding):
			Padding_Byte += "\x00"
		MAC = binascii.a2b_hex(hashlib.md5(DB_ID + Msg_ID + Data_Len + Data_Cont + Padding_Byte).hexdigest())
		return DB_ID + Msg_ID + Data_Len + Data_Cont + Padding_Byte + MAC

	def set_Data_Section(self):
		Proto_Ver = "\x01"
		Crypt_Ver_and_Key_Type = "\x06"
		OPE_ID = "\xff\xff"
		SMS_ID = "\x00\x01"
		Data_Body = self.set_Data_Body()
		DB_Len = struct.pack('>H',len(Data_Body))
		return Proto_Ver + Crypt_Ver_and_Key_Type + OPE_ID + SMS_ID + DB_Len + Data_Body

class analysis_yongxin_osd_response(object):
	def __init__(self, yongxin_osd_response):
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
