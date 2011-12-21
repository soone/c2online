#-*-coding:utf-8-*-
from modules import vcs
from conf import config
import hashlib
import os
import pysvn

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
		self.sourceDir = self.tempPackDir + '/source'
		#打包前准备
		self.expack(vList)
		#从版本库导出文件
		self.vcsExport(vList)
		#压缩并打包和清理
		self.clear()
		return True

	def expack(self, vList):
		'''打包前准备工作'''
		#创建目录
		if os.path.isdir(self.tempPackDir):
			os.system('rm -rf %s' % self.tempPackDir)
		os.system('mkdir -p %s/source' % self.tempPackDir)
		os.system('mkdir -p %s/backup' % self.tempPackDir)
		os.system('mkdir -p %s/bin' % self.tempPackDir)

		#根据列表生成files.log文件
		logfile = ['%s::%s' % (l['f_action'], l['f_path']) for l in vList]
		fdb = open('%s/bin/%s' % (self.tempPackDir, config.PACKAGEFILES), 'w+')
		fdb.write('\n'.join(logfile))
		fdb.close()

	def vcsExport(self, vList):
		'''从版本库导出'''
		for l in vList:
			self.pv.export(sourceUrl = '%s%s' % (self.hostUrl, l['f_path']), destPath = '%s/source%s' % (self.tempPackDir, l['f_path']), ver = l['f_ver'])

		return True

	def clear(self):
		'''压缩文件并打包，清除临时目录'''
		os.system('tar czvf %s.tar.gz -C %s ./' % (self.tempPackDir, self.tempPackDir))
		os.system('rm -rf %s' % self.tempPackDir)
