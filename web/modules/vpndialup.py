#!/usr/bin/env python
#-*-coding=utf-8-*-
import os
import hashlib

class VpnDialUp:
	def __init__(self):
		pass

	def pptpStart(self, host, user, pw):
		'''pptp拨号'''
		pptpName = hashlib.new('md5', host).hexdigest()[8 : -8]
		rs = os.popen('pptpsetup --create %s --server %s --username %s --password %s --encrypt --start' % (pptpName, host, user, pw))
		print rs.readlines()

	def pptpStop(self, host):
		'''pptp拨号关闭'''
		pass
