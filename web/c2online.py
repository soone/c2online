#/bin/env python
#^-^coding:utf-8^-^

import web

urls = (
	'/',  'LoginForm',
	'/login', 'LoginGo',
	'/logout', 'Logout',
	'/my', 'MyIndex',
	'/net', 'ReleaseNet',
	'/com', 'ReleaseCom',
	'/project', 'ProjectManage',
	'/edit', 'ProjectEdit',
	'/add', 'ProjectAdd',
	'/del', 'ProjectDel'
)

c2online = web.application(urls, globals())

class LoginForm(object):
	def GET(self):
		print 'a'

if __name__ == "__main__":
	c2online.run()
