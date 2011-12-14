#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
import dbHelp

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/', 'Create',
		'/list/', 'List',
		'/change/', 'Change',
		'/update/', 'Update',
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
	def GET(self, action):
		pass

	def POST(self):
		inputs = web.input()
		if self.emptyValide(inputs['pname']) is False or \
			self.emptyValide(inputs['vcs']) is False or \
			self.emptyValide(inputs['vcsuser']) is False or \
			self.emptyValide(inputs['vcspass']) is False:
			return json.dumps({'res' : 0, 'msg' : '各项不能为空'})

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			res = db.insert('c2_project', p_name = inputs['pname'].strip(), \
			p_vcspath = inputs['vcs'].strip(), \
			p_user = inputs['vcsuser'].strip(), \
			p_pass = inputs['vcspass'].strip(), \
			p_cdateline = time.time(), \
			p_status = 1)

			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

	def emptyValide(self, arg):
		return len(arg) > 0 or arg == True

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
		if inputs['name'] is None or \
			inputs['id'] is None or \
			inputs['val'] is None:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#修改数据
		try:
			name = inputs['name'].strip()
			id = inputs['id'].strip()
			val = inputs['val'].strip()
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#db.update('c2_project', name = $val, where = 'p_id = $db', vars = locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})
		return json.dumps({'res' : 1})
