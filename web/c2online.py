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

logUserInfo = {}
def onload(handler):
	web.ctx.session = session
	try:
		global logUserInfo
		logUserInfo = {'uName' : web.ctx.session.uName, 'uAuth' : web.ctx.session.uAuth, 'uId' : web.ctx.session.uId}
	except:
		return handler()

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
		return render.index(ac=1, logUserInfo = logUserInfo)

if __name__ == "__main__":
	c2online.run()
