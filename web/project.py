#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/', 'Create'
        )
render = config.render
appProject = web.application(urls, globals())

class ReProject:
	def GET(self): raise web.redirect('/')

class Project:
    def GET(self):
        plist = ['test']
        return render.project(plist = plist)

class Create:
	def GET(self, action):
		pass

	def POST(self):
		print web.input()
		pass
