#/bin/env python
#-*-coding:utf-8-*-

import web
from conf import config

urls = (
	'/',  'Index',
	'/index',  'Index',
)
render = config.render
c2online = web.application(urls, globals())

class Index(object):
	def GET(self):
		return render.index(ac=1)

if __name__ == "__main__":
	c2online.run()
