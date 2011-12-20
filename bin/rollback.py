#!/bin/env python
#!-*-coding:utf-8-*-
import os
import sys
FILELOG = 'files.log'
PRESHELL = 'pre.sh'
class Rollback:
	def __init__(self):
		self.verNo = sys.argv[1]
		self.relDir = sys.argv[2]
		self.wwwDir = sys.argv[3]
		#解压压缩包
		os.system('tar zxvf %s/%s.tar.gz -C %s/%s' % (self.relDir, self.verNo, self.relDir, self.verNo))
		self.curSource = self.relDir + '/' + self.verNo + '/source'
		self.curBackup = self.relDir + '/' + self.verNo + '/backup'
		self.curBin = self.relDir + '/' + self.verNo + '/bin'
		#预发布前执行的脚本
		if os.path.isfile(self.curBin + '/' + PRESHELL):
			os.system('/bin/bash %s/%s' % (self.curBin, PRESHELL))

		self.binFile = self.curBin + '/' + FILELOG
		self.lines = []
		if os.path.isfile(self.binFile):
			log = open(self.binFile, 'r')
			self.logLine = log.readlines()
			log.close()
			if len(self.logLine) > 0:
				for line in self.logLine:
					lines = line.strip('\n').split('::')
					self.lines.append([lines[0], lines[1]])

	def rollBack(self):
		'''回滚该版本'''
		if len(self.lines) > 0:
			for line in self.lines:
				if line[0] != 'A':
					pass

	def backup(self):
		'''发布前备份'''
		if len(self.lines) > 0:
			for line in self.lines:
				if line[0] != 'A':
					lineDir = line[1][0:line[1].rindex('/')]
					if line[0] == 'D' and os.path.isdir('%s/%s' % (self.wwwDir, line[1])):
						os.system('mkdir -p %s/%s' % (self.curBackup, line[1]))

					if os.path.isdir('%s/%s' % (self.curBackup, lineDir)) is False:
						os.system('mkdir -p %s/%s' % (self.curBackup, lineDir))

					if os.path.isfile('%s/%s' % (self.wwwDir, line[1])):
						os.system('cp %s/%s %s/%s' % (self.wwwDir, line[1], self.curBackup, line[1]))

			return True
		else:
			return False

	def release(self):
		'''开始发布'''
		if len(self.lines) > 0:
			for line in self.lines:
				if line[0] != 'D':
					if line[0] == 'A' and os.path.isdir('%s/%s' % (self.wwwDir, line[1])) is False:
						os.system('mkdir -p %s/%s' % (self.wwwDir, line[1]))

					lineDir = line[1][0:line[1].rindex('/')]
					if os.path.isdir('%s/%s' % (self.wwwDir, lineDir)) is False:
						os.system('mkdir -p %s/%s' % (self.wwwDir, lineDir))

					if os.path.isfile('%s/%s' % (self.curSource, line[1])):
						os.system('cp %s/%s %s/%s' % (self.curSource, line[1], self.wwwDir, line[1]))
				else:
					if os.path.isdir('%s/%s' % (self.wwwDir, line[1]) or os.path.isfile('%s/%s' % (self.wwwDir, line[1]) or os.path.isfile())):
						os.system('rm -rf %s/%s' % (self.wwwDir, line[1]))

			return True
		else:
			return False

	def clear(self):
		'''重新打包已经备份的文件和发布的文件'''
		os.system('rm -rf %s/%s.tar.gz' % (self.relDir, self.verNo))
		os.system('tar zcvf %s/%s.tar.gz -C %s/%s ./' % (self.relDir, self.verNo, self.relDir, self.verNo))
		os.system('rm -rf %s/%s' % (self.relDir, self.verNo))
		return True

def usage():
	print 'Usage:python release.py 2.0.15.r8888 /data/server/a0b923820dcc509a /data/wwwV2'

if __name__ == '__main__':
	if len(sys.argv) < 4:
		usage()
		sys.exit(2)

	ser = Server()

	print '发布前备份文件...'
	if ser.backup() == False:
		print 'log文件不存在，备份失败'
		sys.exit(2)

	print '开始发布...'
	if ser.release() == False:
		print ''
		sys.exit(2)
	print '发布清理...'
	ser.clear()
