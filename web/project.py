#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids
from modules import vcs

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/', 'Create',
		'/list/', 'List',
		'/change/', 'Change',
		'/update/', 'Update',
		'/vcslist/', 'Vcslist',
        )
render = config.render
appProject = web.application(urls, globals())

class ReProject:
	def GET(self): raise web.redirect('/')

class Project:
    def GET(self):
		'''取数据库项目信息'''
		dbase = dbHelp.DbHelp()
		db = dbase.database()
		plist = db.select('c2_project', order='p_status, p_cdateline desc')
		if len(plist) == 0:
			plist = ''
		return render.project(plist = plist)

class Create:
	def POST(self):
		inputs = web.input()
		name = inputs['pname'].strip()
		vcspath = inputs['vcs'].strip()
		vcsuser = inputs['vcsuser'].strip()
		vcspass = inputs['vcspass'].strip()
		v = valids.Valids()

		if v.isEmpty(name) or \
			v.isEmpty(vcspath) or \
			v.isEmpty(vcsuser) or \
			v.isEmpty(vcspass):
			return json.dumps({'res' : 0, 'msg' : '各项不能为空'})

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			res = db.insert('c2_project', p_name = name, \
			p_vcspath = vcspath, \
			p_user = vcsuser, \
			p_pass = vcspass, \
			p_cdateline = time.time(), \
			p_status = 1)

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
			db.update('c2_project', p_status = status, where = 'p_id IN $ids', vars=locals())
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
			if name == 'vcs':
				dVal = {'p_vcspath' : val}
			elif name == 'vcsuser':
				dVal = {'p_user' : val}
			elif name == 'vcspass':
				dVal = {'p_pass': val}
			else:
				return json.dumps({'res' : 0, 'msg' : '数据不合法'})

			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_project', where = 'p_id = $id', vars = locals(), **dVal)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})
		return json.dumps({'res' : 1})

class Vcslist:
	def POST(self):
		inputs = web.input()
		vids = inputs['vids'].strip()
		pro = inputs['pro'].strip()
		v = valids.Valids()
		if v.isEmpty(vids) or v.isEmpty(pro):
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		try:
			vidsArr = [int(x) for x in vids.split('|')]
		except:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		vidsArr.sort()

		#查找项目信息
		#try:
		dbase = dbHelp.DbHelp()
		db = dbase.database()
		res = db.select('c2_project', what = 'p_vcspath, p_user, p_pass', where = 'p_id = $pro AND p_status = 1', vars = locals())
		if len(res) == 0:
			raise Error

		rs = res[0]
		pv = vcs.Vcs(vPath = rs.p_vcspath, vUser = rs.p_user, vPass = rs.p_pass)
		return json.dumps({'res' : 1, 'text':pv.getLog(vidsArr)})
		#except:
		#	return json.dumps({'res' : 0, 'msg' : '系统错误'})
