#!/usr/bin/env python
#-*-coding=utf-8-*-
import pexpect
import pxssh
from conf import config
import subprocess
import hashlib

class SerLink:
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
		if self.vpnType == 1:
			child = pexpect.spawn(config.PPTPCONNECTCMD % (hashlib.new('md5', self.vpn).hexdigest()[8 : -8], self.vpn, self.vpnUser, self.vpnPw))
			child.sendline('181633139')
			#child.sendline('sudo /sbin/route add -net 192.168.10.0 netmask 255.255.255.0 dev ppp0')

		child.expect(pexpect.EOF)
		res = child.before.replace('\n', '<br />')
		return res

	def vpnClose(self):
		'''vpn关闭'''
		if self.vpnType == 1:
			child = pexpect.spawn(config.PPTPCLOSECMD % hashlib.new('md5', self.vpn).hexdigest()[8 : -8])
			child.sendline('181633139')

		child.expect(pexpect.EOF)
		res = child.before.replace('\n', '<br />')
		return res

	def scpSend(self, files):
		'''scp发送文件'''
		fs = ' '.join(files)
		scpCmd = 'scp -r %s %s@%s:%s' % (fs, self.user, self.host, self.bdir)
		child = pexpect.spawn(scpCmd)
		i = child.expect([pexpect.TIMEOUT, 'password: '])
		if i == 0:
			return 'ERROR!'
		
		child.sendline(self.pw)
		child.expect(pexpect.EOF)
		return True

	def sshRelese(self, verNos):
		'''登录目标服务器运行发布脚本'''
		client = pxssh.pxssh()
		client.login(self.host, self.user, self.pw)
		client.sendline('python %s%s "%s" %s %s' % (self.bdir, config.RELEASENAME, ' '.join(verNos), self.bdir, self.pdir))
		client.prompt()
		rlog = client.before
		client.logout()
		return rlog.replace('\n', '<br />')
