#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/(.*)', 'Create'
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
		return json.dumps({"a1":11, "a2":22})

	def POST(self, args):
		return json.dumps({"a1":1, "a2":2})
