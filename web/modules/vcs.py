#!/usr/bin/env python
#-*-coding=utf-8-*-
import pysvn
import os

class Vcs(object):
	'''用来从版本控制系统中提取要发布到文件列表'''
	def __init__(self, vPath, vUser, vPass):
		self.vPath = vPath
		self.vUser = vUser
		self.vPass = vPass
		self.client = pysvn.Client()
		self.client.callback_get_login = self.getLogin
		self.preLen = len(self.vPath[len(self.client.root_url_from_path(self.vPath)):])

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
                #logs.append([v, [[l.action, l.path[self.preLen:]] for l in ls[0].changed_paths]])
				print([v, [[l.action, l.path[self.preLen:]] for l in ls[0].changed_paths]])
                print(ls[0].change_paths)

		return logs

	def export(self, sourceUrl, destPath, ver):
		'''按照版本号和路径导出'''
		destDir = destPath[0:destPath.rindex('/')]
		if os.path.isdir(destDir) is False:
			os.system('mkdir -p %s' % destDir)

		self.client.export(sourceUrl, destPath, revision = pysvn.Revision(pysvn.opt_revision_kind.number, ver))
