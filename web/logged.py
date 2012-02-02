#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
from modules import dbHelp
from modules import valids
import json
import hashlib

urls = (
        '/login/',  'Login',
		'/logout/', 'Logout',
		'/users/', 'UserList',
		'(.*)', 'ReIndex',
)

render = config.render
appLogged = web.application(urls, globals())

class ReIndex(object):
	def GET(self): raise web.redirect('/', True)

class Login(object):
	def POST(self):
		inputs = web.input()
		user = inputs['user'].strip()
		pwd = inputs['pass'].strip()
		v = valids.Valids()

		if v.isEmpty(user) or v.isEmpty(pwd) or len(user) > 12 or len(user) < 5 or len(pwd) > 24 or len(pwd) < 6:
			return json.dumps({'res' : 0, 'msg' : 'Oops...请填写正确的用户名和密码'})

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看用户是否真实存在
			res = db.select('c2_admin', what = '*', where = 'adm_user = $user', limit = 1, vars = locals())
			if len(res) < 1:
				return json.dumps({'res' : 0, 'msg' : 'Oops...用户名或密码错误'})

			uInfo = res[0]

			if uInfo.adm_status != 1:
				return json.dumps({'res' : 0, 'msg' : 'Oops...该用户已经被禁用'})

			if uInfo.adm_pass != hashlib.new('md5', '%s%s' % (user, pwd)).hexdigest():
				return json.dumps({'res' : 0, 'msg' : 'Oops...用户名或密码错误'})

			#设置session
			web.ctx.session.uId = uInfo.adm_id
			web.ctx.session.uName = uInfo.adm_user
			web.ctx.session.uAuth = uInfo.adm_auth
			return json.dumps({'res' : 1, 'uInfo' : [uInfo.adm_id, uInfo.adm_user, uInfo.adm_auth]})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Logout(object):
	def GET(self):
		'''直接删除session'''
		try:
			web.ctx.session.kill()
		except:
			pass
		return json.dumps({'res' : 1, 'redirect' : '/'})
