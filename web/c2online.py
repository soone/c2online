#/bin/env python
#-*-coding:utf-8-*-

import web
from conf import config
import project
import servers
import logged
import re
import json
from modules import dbHelp

urls = (
	'/servers', servers.appServers,
    '/project', project.appProject,
	'/logged', logged.appLogged,
	'/users', 'UserList',
	'/(.*)',  'Index',
)

def onload(handler):
	web.ctx.session = session
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

if __name__ == "__main__":
	c2online.run()
