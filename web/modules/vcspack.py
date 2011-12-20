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
		self.verNo = verNo
		self.tempPackDir = self.dirs + self.verNo
		#打包前准备
		self.expack()
		#从版本库导出文件
		self.vcsExport(vList)
		#压缩

		#打包后清理
		self.clear()
		return True

	def expack(self):
		'''打包前准备工作'''
		#创建目录
		if os.path.isdir(self.tempPackDir):
			os.system('rm -rf %s' % self.tempPackDir)
		os.system('mkdir -p %s/source' % self.tempPackDir)
		os.system('mkdir -p %s/backup' % self.tempPackDir)
		os.system('mkdir -p %s/bin' % self.tempPackDir)

		#根据列表生成fdb.py文件
		fdb = open('%s/bin/%s', )

	def vcsExport(self, vList):
		pass

	def clear(self):
		pass
