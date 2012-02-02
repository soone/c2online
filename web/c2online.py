#/bin/env python
#-*-coding:utf-8-*-

import web
from conf import config
import project
import servers
import logged
import json
from modules import dbHelp
from modules import valids
import hashlib
import time

urls = (
	'/servers', servers.appServers,
    '/project', project.appProject,
	'/logged', logged.appLogged,
	'/users', 'UserList',
	'/users/set', 'UserSetStatus',
	'/users/pwd', 'UserSetPwd',
	'/users/add', 'UserAdd',
	'/(.*)',  'Index',
)

def onload(handler):
	web.ctx.session = session
	try:
		web.ctx.session.uName is None
	except:
		if web.ctx.env['PATH_INFO'] in ['/users', '/users/set', '/users/pwd', '/users/add']:
			if 'HTTP_X_REQUESTED_WITH' in web.ctx.environ and web.ctx.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
				return json.dumps({'res' : 'error', 'msg' : '您已经退出登录，请<a href="/index?login">重新登录</a>'})
			else:
				web.seeother('/index?login', True)

	return handler()

render = config.render
c2online = web.application(urls, globals())
c2online.add_processor(onload)
#session = web.session.Session(c2online, web.session.DiskStore(config.SESSIONSTORE))
if web.config.get('_session') is None:
	session = web.session.Session(c2online, web.session.DiskStore(config.SESSIONSTORE))
	web.config._session = session
else:
	session = web.config._session

class Index(object):
	def GET(self, path):
		return render.index(ac=1, logUserInfo = web.ctx.session)

class UserList:
	def GET(self):
		'''取管理员列表'''
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			uId = web.ctx.session.uId
			uAuth = web.ctx.session.uAuth
			if uAuth == 1:
				ulist = db.select('c2_admin', what = 'adm_id, adm_user, adm_dateline, adm_status, adm_auth')
			else:
				ulist = db.select('c2_admin', what = 'adm_id, adm_user, adm_dateline, adm_status, adm_auth', where ='adm_id = $uId', limit = 1, vars = locals())
			if len(ulist) == 0:
				return json.dumps({'res' : 0, 'msg' : 'Oops...系统问题'})

			return json.dumps({'res' : 1, 'users' : [l for l in ulist], 'curId' : uId, 'curAuth' : uAuth})
		except:
			return json.dumps({'res' : 0, 'msg' : 'Oops...请重新刷新页面'})

class UserSetStatus:
	def POST(self):
		inputs = web.input()
		uId = inputs['uId'].strip()
		status = int(inputs['sta'].strip())
		v = valids.Valids()

		if v.isEmpty(uId):
			return json.dumps({'res' : 0, 'msg' : '参数错误'})

		#操作数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_admin', adm_status = status, where = 'adm_id = $uId', vars=locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class UserSetPwd:
	def POST(self):
		inputs = web.input()
		uId = inputs['uId'].strip()
		pwd = inputs['pwd'].strip()
		v = valids.Valids()
		pwdLen = len(pwd)

		if v.isEmpty(uId) or pwdLen < 6 or pwdLen > 12:
			return json.dumps({'res' : 0, 'msg' : '密码长度必须在6－12个字符之间'})

		if web.ctx.session.uAuth != 1 and web.ctx.session.uId != int(uId):
			return json.dumps({'res' : 0, 'msg' : '对不起，你没有权限修改该用户密码'})


		#操作数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			md5Pwd = hashlib.new('md5', '%s%s' % (web.ctx.session.uName, pwd)).hexdigest()
			if web.ctx.session.uId != uId:
				uInfo = db.select('c2_admin', what = 'adm_user', where = 'adm_id= $uId', limit = 1, vars = locals())
				if len(uInfo) < 1:
					return json.dumps({'res' : 0, 'msg' : '对不起，该用户不存在'})

				md5Pwd = hashlib.new('md5', '%s%s' % (uInfo[0].adm_user, pwd)).hexdigest()

			db.update('c2_admin', adm_pass = md5Pwd, where = 'adm_id = $uId', vars=locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class UserAdd:
	def POST(self):
		inputs = web.input()
		uName = inputs['uName'].strip()
		pwd = inputs['pwd'].strip()
		v = valids.Valids()
		pwdLen = len(pwd)
		nameLen = len(uName)

		if v.isEmpty(uName) or nameLen < 4 or nameLen > 12:
			return json.dumps({'res' : 0, 'msg' : '登录名长度必须在6－12个字符之间'})

		if v.isEmpty(pwd) or pwdLen < 6 or pwdLen > 12:
			return json.dumps({'res' : 0, 'msg' : '密码长度必须在6－12个字符之间'})

		if web.ctx.session.uAuth != 1:
			return json.dumps({'res' : 0, 'msg' : '对不起，你没有权限添加用户'})


		#操作数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看用户是否存在
			existUser = db.select('c2_admin', what = 'adm_id', where = 'adm_user = $uName', limit = 1, vars = locals())
			if len(existUser) > 0:
				return json.dumps({'res' : 0, 'msg' : '用户已经存在'})

			md5Pwd = hashlib.new('md5', '%s%s' % (uName, pwd)).hexdigest()
			db.insert('c2_admin', adm_user = uName, adm_pass = md5Pwd, adm_dateline = time.time())
			return json.dumps({'res' : 1, 'msg' : '用户添加成功，请点击设置重新读取用户列表'})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

if __name__ == "__main__":
	c2online.run()
