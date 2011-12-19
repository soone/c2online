#-*-coding:utf-8-*-
from modules import vcs
from conf import config
import hashlib
import os

class VcsPack:
	'''专门打包从版本库抽象出来的文件'''
	def __init__(self, **v):
		self.dirs = config.PACKAGEROOT % (hashlib.new('md5', v['vid']).hexdigest()[8:-8])
		self.pv = vcs.Vcs(vPath = v['vpath'], vUser = v['vuser'], vPass = v['vpass'])
		self.hostUrl = v['vpath']

	def goPack(self, vList, verNo):
		'''开始打包'''
		self.tempPackDir = self.dirs + verNo
		#打包前准备
		self.expack()
		#先生成shell文件
		self.packShell(vList)
		#从版本库导出文件
		self.vcsExport(vList)
		#压缩

		#打包后清理
		self.clear(verNo)
		return True

	def expack(self):
		'''打包前准备工作'''
		if os.path.isdir(self.tempPackDir):
			os.system('rm -rf %s' % self.tempPackDir)

		os.system('mkdir %s' % self.tempPackDir)

	def packShell(self, vList):
		'''生成shell文件'''
		print vList
		f = open(self.tempPackDir + '/' + config.PACKAGESHELL, 'a+')
		for l in vList:
			pass

	def vcsExport(self, vList):
		pass
