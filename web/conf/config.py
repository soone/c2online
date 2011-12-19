#-*-coding:utf-8-*-
CHARSET = 'utf-8'

from web.contrib.template import render_mako
import os.path

render = render_mako(
	directories = ['templates'],
	input_encoding = CHARSET,
	output_encoding = CHARSET
	)

DBINFO = {
	'host' : '127.0.0.1',
	'db' : 'c2online',
	'user' : 'root',
	'pw' : '123456',
	'dbn' : 'mysql'
	}

#打包根目录
PACKAGEROOT = os.path.abspath('../') + "/packdir/%s/"
PACKAGESHELL = 'preshell.sh'
