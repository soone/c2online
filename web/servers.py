#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids
import sys

urls = (
		'', 'ReServers',
        '/',  'Servers',
		'/create/', 'Create',
		'/change/', 'Change',
		'/update/', 'Update',
		'/test/(.*)', 'Test',
		'/test1/', 'Test1',
        )
render = config.render
appServers = web.application(urls, globals())

class ReServers:
	def GET(self): raise web.redirect('/')

class Servers:
	def GET(self):
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			slist = db.select('c2_server', order='s_status, s_cdateline desc')
			if len(slist) == 0:
				slist = ''
			return render.servers(slist = slist, ac = 3)
		except:
			return render.servers(ac = 3)

class Create:
	def POST(self):
		inputs = web.input()
		pId = inputs['pid'].strip()
		sname = inputs['sname'].strip()
		pdir = inputs['pdir'].strip()
		bdir = inputs['bdir'].strip()
		spath = inputs['spath'].strip()
		suser = inputs['suser'].strip()
		spass = inputs['spass'].strip()
		v = valids.Valids()

		if v.isEmpty(pId) or \
			v.isEmpty(sname) or \
			v.isEmpty(pdir) or \
			v.isEmpty(bdir) or \
			v.isEmpty(spath) or \
			v.isEmpty(suser) or \
			v.isEmpty(spass):
			return json.dumps({'res' : 0, 'msg' : '带*不能为空'})

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看是否重名
			rs = db.select('c2_server', what = 's_id', where = 's_name = $sname', limit = 1, vars = locals())
			if len(rs) > 0:
				return json.dumps({'res' : 0, 'msg' : '该服务器名称已经存在'})

			pData = {'p_id' : pId, 
					's_name' : sname, 
					's_host' : spath, 
					's_user' : suser, 
					's_pass' : spass, 
					's_pdir' : pdir, 
					's_bdir' : bdir, 
					's_cdateline' : time.time(), 
					's_status' : 1}
			if 'svpn' in inputs:
				pData['s_vpn'] = inputs['svpn'].strip()

			if 'svpnname' in inputs:
				pData['s_vpnuser'] = inputs['svpnname'].strip()

			if 'svpnpass' in inputs:
				pData['s_vpnpass'] = inputs['svpnpass'].strip()

			res = db.insert('c2_server', **pData)

			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

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

		if v.isEmpty(name) or \
			v.isEmpty(id) or \
			v.isEmpty(val):
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

class Test1:
	def GET(self):
		return render.servers(ac = 3)

class Test:
	def GET(self, count):
		web.header('Content-type', 'text/html;charset=UTF-8')
		web.header("Cache-Control", "no-cache, must-revalidate")
		web.header("Expires", "Mon, 26 Jul 1997 05:00:00 GMT")
		for i in range(50):
			time.sleep(1)
			yield str(i) + "<br/>"
