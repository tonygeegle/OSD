#!/usr/bin/python
# -*- coding: UTF-8 -*-
#创建日期：2015.06.10
import struct
import re

class set_shuma_osd_request(object):
	"""
	Data_Section
	  |--SessionID
	  |--CAS_Ver
	  |--Command_Type
	  |--Data_Len
	  |--Data_Body
	      |--Card_ID
	      |--Show_Time_Len
	      |--Show_Times
	      |--Priority
	      |--Expired_Time
	      |--Data_Len
	      |--Data_Body_content
	"""
	def __init__(self, \
			SessionID = 1, \
			Card_ID = "12345678", \
			Data_content = "abcd", \
			Show_Time_Len = 0, \
			Show_Times = 1, \
			Priority = 0, \
			Expired_Time = 1433076891):
		self.error_reason = None
		self.SessionID = int(re.findall(r"\d+",str(SessionID))[0])
		self.Card_ID = int(re.findall(r"\d{8}",str(Card_ID))[0]) # 8位内部卡号
		self.Data_content = str(Data_content)
		self.Show_Time_Len = int(re.findall(r"\d+",str(Show_Time_Len))[0]) # 显示多少秒
		self.Show_Times = int(re.findall(r"\d+",str(Show_Times))[0]) # 显示多少次
		self.Priority = int(re.findall(r"\d+",str(Priority))[0])
		self.Expired_Time = int(re.findall(r"\d+",str(Expired_Time))[0]) # 过期时间，一般是当前时间的一小时后
		re.purge()

	def set_Data_Body(self):
		Card_ID = struct.pack('>L', int(self.Card_ID)) # 4字节，内部卡号
		Show_Time_Len = struct.pack('>H', self.Show_Time_Len) # 2字节，为0时按照显示次数显示
		Show_Times = struct.pack('>B', self.Show_Times) # 1字节
		Priority = struct.pack('>B', self.Priority) # 1字节
		Expired_Time = struct.pack('>L', self.Expired_Time) # 4字节
		Data_content = str(self.Data_content)
		Data_Len = struct.pack('>B',len(Data_content)) # 1字节
		return Card_ID + Show_Time_Len + Show_Times + Priority + Expired_Time + Data_Len + Data_content

	def set_Data_Section(self):
		SessionID = str(struct.pack('>H',self.SessionID))
		CAS_Ver = "\x02"
		Command_Type = "\x02"
		Data_Body = str(self.set_Data_Body())
		Data_Len = str(struct.pack('>H',len(Data_Body)))
		return SessionID + CAS_Ver + Command_Type + Data_Len + Data_Body

class analysis_shuma_osd_response(object):
	"""
	Data_Section
	  |--SessionID
	  |--CAS_Ver
	  |--Command_Type
	  |--Data_Len
	  |--Data_Body
	      |--errocode
	"""
	def __init__(self, shuma_osd_response):
		self.error_reason = None
		self.shuma_osd_response = shuma_osd_response
		self.get_body_from_section()

	def get_body_from_section(self):
		self.SessionID = self.shuma_osd_response[0:2]
		self.CAS_Ver = self.shuma_osd_response[2:3]
		self.Command_Type = self.shuma_osd_response[3:4]
		self.Data_Len = self.shuma_osd_response[4:6]
		self.Data_Body = self.shuma_osd_response[6:]
		if len(self.Data_Body) != struct.unpack('>H', self.Data_Len)[0]: # 判断长度是否正常
			self.error_reason = "Response bits length error"
			print "\t\t" + self.error_reason
			return "ERROR"
		return self.Data_Body

	def get_errocode_from_content(self):
		self.errocode = self.Data_Body
		if "\x00\x00\x00\x00" == self.errocode:
			return "执行成功"
		else:
			return str(self.errocode)
#a = analysis_shuma_osd_response("\x00\x04\x02\x02\x00\x04\x00\x00\x00\x00")
#print repr(a.get_errocode_from_content())
