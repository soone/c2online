#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids

urls = (
		'', 'ReServers',
        '/',  'Servers',
		'/create/', 'Create',
		'/change/', 'Change',
		'/update/', 'Update',
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
