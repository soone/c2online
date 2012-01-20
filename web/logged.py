#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
from modules import dbHelp
from modules import valids
import json
import time
import hashlib

urls = (
        '/login/',  'Login',
		'(.*)', 'ReIndex',
)

render = config.render
appLogged = web.application(urls, globals())

class ReIndex:
	def GET(self): raise web.redirect('/index')

class Login:
	def POST(self):
		inputs = web.input()
		user = inputs['user'].strip()
		pwd = inputs['pass'].strip()
		v = valids.Valids()

		if v.isEmpty(user) or v.isEmpty(pwd) or len(user) > 12 or len(user) < 5 or len(pwd) > 24 or len(pwd) < 6:
			return json.dumps({'res' : 0, 'msg' : 'Oops...请填写正确的用户名和密码'})

		#入库操作
		#try:
		dbase = dbHelp.DbHelp()
		db = dbase.database()
		#查看用户是否真实存在
		res = db.select('c2_admin', what = '*', where = 'adm_user = $user', limit = 1, vars = locals())
		if len(res) < 1:
			return json.dumps({'res' : 0, 'msg' : 'Oops...用户名或密码错误'})

		uInfo = res[0]

		if uInfo.adm_status == 2:
			return json.dumps({'res' : 0, 'msg' : 'Oops...该用户已经被禁用'})

		if uInfo.adm_pass != hashlib.new('md5', '%s%s' % (user, pwd)).hexdigest():
			return json.dumps({'res' : 0, 'msg' : 'Oops...用户名或密码错误'})

		#设置session
		web.ctx.session.uId = uInfo.adm_id
		web.ctx.session.uName = uInfo.adm_user
		web.ctx.session.uAuth = uInfo.adm_auth
		return json.dumps({'res' : 1, 'uInfo' : [uInfo.adm_id, uInfo.adm_user, uInfo.adm_auth]})
		#except:
			#return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Change:
	def POST(self):
		inputs = web.input()
		status = 1
		if len(inputs['checkboxs']) == 0:
			return json.dumps({'res' : 0, 'msg' : '请至少选择一项'})

		if len(inputs['status']) > 0:
			status = inputs['status'].strip()

		#修改数据库
		try:
			ids = inputs['checkboxs'].strip().split('|')
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_server', s_status = status, where = 's_id IN $ids', vars=locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Update:
	def POST(self):
		inputs = web.input()
		name = inputs['name'].strip()
		id = inputs['id'].strip()
		val = inputs['val'].strip()
		v = valids.Valids()

		if (v.isEmpty(name) or \
			v.isEmpty(id) or \
			v.isEmpty(val)) and name.find('vpn') == -1:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#修改数据
		try:
			if name == 'pdir':
				dVal = {'s_pdir' : val}
			elif name == 'bdir':
				dVal = {'s_bdir' : val}
			elif name == 'host':
				dVal = {'s_host': val}
			elif name == 'user':
				dVal = {'s_user': val}
			elif name == 'pass':
				dVal = {'s_pass': val}
			elif name == 'vpn':
				dVal = {'s_vpn': val}
			elif name == 'vpnuser':
				dVal = {'s_vpnuser': val}
			elif name == 'vpnpass':
				dVal = {'s_vpnpass': val}
			else:
				return json.dumps({'res' : 0, 'msg' : '数据不合法'})

			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_server', where = 's_id = $id', vars = locals(), **dVal)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class ShortList:
	def GET(self, pId):
		'''取数据库服务器列表信息'''
		v = valids.Valids()
		pId = pId.strip()
		if v.isEmpty(pId):
			return json.dumps({'res' : 0, 'msg' : '参数不合法'})

		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			plist = db.select('c2_server', what = 's_id, s_name', where = 's_status = 1 AND p_id = $pId', order='s_cdateline desc', vars = locals())
			if len(plist) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无服务器列表，请先创建服务器'})

			return json.dumps({'res' : 1, 'list' : [l for l in plist]})
		except:
			return json.dumps({'res' : 0, 'msg' : '服务器列表读取失败'})

class History:
	def GET(self, sId, page = None):
		'''取数据库发布列表信息'''
		v = valids.Valids()
		sId = sId.strip()
		if v.isEmpty(sId):
			return json.dumps({'res' : 0, 'msg' : '参数不合法'})

		if page == '':
			page = 1

		page = int(page)

		eachPage = 10

		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看发布总数
			ct = db.select('c2_log', what = 'COUNT(*) AS c', where = 's_id = $sId', vars = locals())
			allNums = ct[0].c
			if allNums <= 0: 
				return json.dumps({'res' : 0, 'msg' : '暂无发布历史'})

			#最大页数
			maxPage = int(math.ceil(float(allNums)/eachPage))
			if page > maxPage:
				page = maxPage

			slist = db.select('c2_log', what = '*', where = 's_id = $sId', limit = '%d, %d' % ((page-1)*eachPage, eachPage),  order='r_dateline desc', vars = locals())
			if len(slist) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无发布历史'})

			return json.dumps({'res' : 1, 'list' : [l for l in slist], 'maxPage' : maxPage})
		except:
			return json.dumps({'res' : 0, 'msg' : '发布历史列表读取失败'})
