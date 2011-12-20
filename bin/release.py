#!/bin/env python
#!-*-coding:utf-8-*-
import sys
FILELOG = './files.log'
def backup():
	'''发布前备份'''
	pass

def release():
	'''开始发布'''
	pass

def clear():
	pass

def usage():
	print 'Usage:python release.py /data/release/packdir/a0b923820dcc509a /data/wwwV2'

if __name__ == '__main__':
	if len(sys.argv) < 3:
		usage()
		sys.exit(2)

	relDir = sys.argv[1]
	wwwDir = sys.argv[2]
	print '发布前备份文件...'
	backup(relDir, wwwDir)
	print '开始发布...'
	release(relDir, wwwDir)
	print '发布清理...'
	clear()
