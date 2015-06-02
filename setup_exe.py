#!/usr/bin/python
# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe, sys, os

if len(sys.argv) == 1:
	sys.argv.append("py2exe")

options = {'py2exe':{
		"compressed": 1,
		"optimize": 0, #1和2运行不起来
		'bundle_files': 1,
		"dll_excludes": ["w9xpopen.exe"],
		"packages":["wx.lib.pubsub"]
	}}

setup(
	version = '0.0.1',
	description = 'yongxin OSD发送'.decode('utf8'),
	name = 'OSD',#这儿的参数只能是ASCII字符
	author = 'Leniy'.decode('utf8'),
	options = options,
	zipfile=None,
	data_files = [('res', ['res/author.png',"res/author.ico"]),('', ['testcard.csv'])],
	console = [{'script': "yongxin_osd.py",'icon_resources': [(1, "res/author.ico")]}]
)
