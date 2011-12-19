#!/usr/bin/env python
#-*-coding=utf-8-*-
import re
import pysvn

class Vcs:
	'''用来从版本控制系统中提取要发布到文件列表'''
	def __init__(self, vPath, vUser, vPass):
		self.vPath = vPath
		self.preLen = len(re.findall(r'.*://.+?\/(.*)', self.vPath)[0])
		self.vUser = vUser
		self.vPass = vPass
		self.client = pysvn.Client()
		self.client.callback_get_login = self.getLogin

	def getLogin(self, relam, username, may_save):
		return True, self.vUser, self.vPass, True

	def getLog(self, vers = []):
		'''按照版本号返回版本文件列表'''
		logs = []
		for v in vers:
			ls = self.client.log(self.vPath, 
			discover_changed_paths = True, 
			revision_start = pysvn.Revision(pysvn.opt_revision_kind.number, v), 
			revision_end = pysvn.Revision(pysvn.opt_revision_kind.number, v))
			if len(ls) > 0:
				logs.append([v, [[l.action, l.path[self.preLen:]]for l in ls[0].changed_paths]])

		return logs
