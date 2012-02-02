#!/usr/bin/env python
#-*-coding=utf-8-*-
import pexpect
import pxssh
from conf import config
import subprocess
import hashlib

class SerLink(object):
	'''本地服务器和目标服务器交互的助手类'''
	def __init__(self, **sInfo):
		self.host = sInfo['host']
		self.user = sInfo['user']
		self.pw = sInfo['pw']
		self.bdir =  sInfo['bdir']
		self.pdir = sInfo['pdir']
	
	def vpnConnect(self, **v):
		'''vpn拨号开始'''
		self.vpn = v['vpn']
		self.vpnUser = v['user']
		self.vpnPw = v['pw']
		self.vpnType = v['type']
		self.vpnRoute = v['route'][0 : v['route'].rindex('.')]
		res = []
		if self.vpnType == 1:
			p = subprocess.Popen(config.PPTPCONNECTCMD % (hashlib.new('md5', self.vpn).hexdigest()[8 : -8], self.vpn, self.vpnUser, self.vpnPw), shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			while True:
				rs = p.stdout.readline()
				if rs == '' or p.poll() != None:
					break
				else:
					res.append(rs)

			#添加路由
			print config.PPTPROUTERADD % self.vpnRoute
			subprocess.Popen(config.PPTPROUTERADD % self.vpnRoute, shell = True)

		return ''.join(res).replace('\n', '<br />')

	def vpnClose(self):
		'''vpn关闭'''
		if self.vpnType == 1:
			#去掉路由
			subprocess.Popen(config.PPTPROUTERDEL % self.vpnRoute, shell = True)
			#关闭vpn
			subprocess.Popen(config.PPTPCLOSECMD, shell = True)

		return True

	def scpSend(self, files):
		'''scp发送文件'''
		fs = ' '.join(files)
		scpCmd = 'scp -r %s %s@%s:%s' % (fs, self.user, self.host, self.bdir)
		child = pexpect.spawn(scpCmd)
		i = child.expect([pexpect.TIMEOUT, 'Are you sure you want to continue connecting', 'password: '])
		if i == 0:
			return 'ERROR!'
		elif i == 1:
			child.sendline('yes')

		child.sendline(self.pw)
		child.expect(pexpect.EOF)
		return ''

	def sshRelese(self, verNos):
		'''登录目标服务器运行发布脚本'''
		client = pxssh.pxssh()
		client.login(self.host, self.user, self.pw)
		client.sendline('python %s%s "%s" %s %s' % (self.bdir, config.RELEASENAME, ' '.join(verNos), self.bdir, self.pdir))
		client.prompt()
		rlog = client.before
		client.logout()
		return rlog.replace('\n', '<br />')
