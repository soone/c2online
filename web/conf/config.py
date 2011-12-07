#-*-coding:utf-8-*-
CHARSET = 'utf-8'

from web.contrib.template import render_mako
render = render_mako(
	directories = ['templates'],
	input_encoding = CHARSET,
	output_encoding = CHARSET
	)
