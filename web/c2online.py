#/bin/env python
#-*-coding:utf-8-*-

import web
from conf import config
import project
import servers
import logged
import re

urls = (
	'/servers', servers.appServers,
    '/project', project.appProject,
	'/logged', logged.appLogged,
	'/(.*)',  'Index',
)

def onload(handler):
	if re.match('^(/servers|/project)+(.*)', web.ctx.path) != None:
		#判断登录
		try:
			getattr('session', 'userId')
		except:
			web.redirect('/index?login')

	return handler()

render = config.render
c2online = web.application(urls, globals())
c2online.add_processor(onload)
session = web.session.Session(c2online, web.session.DiskStore(config.SESSIONSTORE), initializer = {'userId' : ''})
#if web.config.get('_session') is None:
#	session = web.session.Session(c2online, web.session.DiskStore(config.SESSIONSTORE), initializer = {'userId' : ''})
#	web.config._session = session
#else:
#	session = web.config._session

class Index(object):
	def GET(self, path):
		return render.index(ac=1)

if __name__ == "__main__":
	c2online.run()
