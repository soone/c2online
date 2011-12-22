#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids
from modules import vcs
from modules import vcspack
import math

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/', 'Create',
		'/change/', 'Change',
		'/update/', 'Update',
		'/vcslist/', 'Vcslist',
		'/package/', 'Package',
		'/packlist/(.+)/(.*)', 'Packlist'
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

		if vcspath[-1] == '/':
			vcspath = vcspath[0:-1]

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
				if val[-1] == '/':
					val = val[0:-1]
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

		vidsArr.sort(reverse = True)

		#查找项目信息
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			res = db.select('c2_project', what = 'p_vcspath, p_user, p_pass', where = 'p_id = $pro AND p_status = 1', vars = locals())
			if len(res) == 0:
				raise Error

			rs = res[0]
			pv = vcs.Vcs(vPath = rs.p_vcspath, vUser = rs.p_user, vPass = rs.p_pass)
			return json.dumps({'res' : 1, 'logs' : pv.getLog(vidsArr)})
		except:
			return json.dumps({'res' : 0, 'msg' : '版本号错误'})

class Package:
	def POST(self):
		inputs = web.input()
		pro = inputs['pro'].strip()
		vals = inputs['vals'].strip()
		verno = inputs['verno'].strip()
		v = valids.Valids()
		if v.isEmpty(pro) or v.isEmpty(vals) or v.isEmpty(verno):
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#插入最新的版本信息并得到该版本对应id
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看项目id是否存在
			res = db.select('c2_project', what = 'p_vcspath, p_user, p_pass', where = 'p_id = $pro AND p_status = 1', limit = '1', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '该项目不存在或者状态不可用'})

			#查看该版本号是否存在
			rNos = db.select('c2_revision', what = '*', where = 'r_no = $verno', vars = locals())
			if len(rNos) > 0:
				return json.dumps({'res' : 0, 'msg' : '该版本号已经存在'})

			rId = db.insert('c2_revision', p_id = pro, \
			r_no = verno, r_cdateline = time.time(), \
			r_status = 1)
			if rId < 1:
				return json.dumps({'res' : 0, 'msg' : '数据库出错'})

			#拆分字符串
			valsArr = vals.split('|')
			valsNum = len(valsArr)
			insValTmp = [dict(zip(['f_ver', 'f_action', 'f_path'], x.split('::'))) for x in valsArr]
			insVal = []
			for x in insValTmp:
				x.update({'r_id' : rId})
				insVal.append(x)

			#插入数据库
			rs = db.multiple_insert('c2_files', insVal)
			if len(rs) != valsNum:
				return json.dumps({'res' : 0, 'msg' : '打包出错，请重试'})

			#真正实际打包到相应位置
			r = res[0]
			vcsPack = vcspack.VcsPack(**{'vpath' : r.p_vcspath, 'vuser' : r.p_user, 'vpass' : r.p_pass, 'vid' : pro})
			vcsPack.goPack(insVal, verno)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统出错'})

class Packlist:
	def GET(self, pro, page = None):
		v = valids.Valids()
		if v.isEmpty(pro) or int(pro) == 0:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		if page == '':
			page = 1

		eachPage = 10
		#查找数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看项目id是否存在
			res = db.select('c2_project', what = 'p_id', where = 'p_id = $pro AND p_status = 1', limit = '1', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '该项目不存在或者状态不可用'})

			#查看打包总数
			ct = db.select('c2_revision', what = 'COUNT(*) AS c', where = 'p_id = $pro', limit = '1', vars = locals())
			allNums = ct[0].c
			if allNums <= 0: 
				return json.dumps({'res' : 0, 'msg' : '暂无已经打包的列表'})

			#最大页数
			maxPage = int(math.ceil(float(allNums)/eachPage))
			if page > maxPage:
				page = maxPage

			#查看该项目下的打包记录
			rs = db.select('c2_revision', what = 'r_no, s_id, s_name, r_dateline, r_cdateline, r_status', where = 'p_id = $pro', limit = '%d, %d' % ((page-1)*eachPage, eachPage), vars = locals())
			if len(rs) == 0:
				return json.dumps({'res' : 0, 'msg' : '已经没有数据了'})

			return json.dumps({'res' : 1, 'list' : [r for r in rs]})
		except:
			return json.dumps({'res' : 0, 'msg' : '读取失败，请刷新'})
