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
				Card_ID = "8370810123456789", \
				Show_Time_Len = 0, \
				Show_Times = 1, \
				Priority = 3, \
				Expired_Time = ""):
		self.SessionID = int(re.findall(r"\d+",str(SessionID))[0])
		self.Card_ID = str(re.findall(r"\d{8}",str(Card_ID))[0]) # 8位内部卡号
		self.Show_Times = Show_Times
		self.Priority = int(Priority)

	def set_Data_Body(self):
		Card_ID = struct.pack('>L', self.Card_ID) # 4字节，内部卡号
		Show_Time_Len = "\x00\x00" # 2字节，为0时按照显示次数显示
		Show_Times = "\x01" # 1字节
		Priority # 1字节
		Expired_Time # 4字节
		Data_content = "测试"
		Data_Len = struct.pack('>H',len(Data_content)) # 1字节
		return 

	def set_Data_Section(self):
		CAS_Ver = "\x02"
		Command_Type = "\x02"
		Data_Body = str(self.set_Data_Body())
		Data_Len = str(struct.pack('>H',len(Data_Body)))
		return self.SessionID + CAS_Ver + Command_Type + Data_Len + Data_Body
a = set_shuma_osd_request()
