#-*-coding:utf-8-*-
CHARSET = 'utf-8'

from web.contrib.template import render_mako
import os.path
import web

web.config.session_parameters['cookie_name'] = 'c2onlineSessionId' #保存session id的cookie的名称
web.config.session_parameters['cookie_domain'] = None #保存session id的Cookie的domain的信息
web.config.session_parameters['timeout'] = 1800 #session的有效时间，以秒为单位
web.config.session_parameters['ignore_expiry'] = True #如果为True，session永不过期
web.config.session_parameters['ignore_change_ip'] = True #如果为True，则表明只有在访问该session的IP与创建该session的ip完全一致时，才被允许访问
web.config.session_parameters['secret_key'] = 'fLjUf2*feRiU3#' #密码种子，为session加密提供一个字符串种子
web.config.session_parameters['expired_message'] = '对不起，会话过期，请重新登录' #session过期时显示的提示信息

SESSIONSTORE = '/tmp/sessions'

web.config.debug = True #关闭调试模式

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
PACKAGEFILES = 'files.log'
#发布的脚本名称
RELEASENAME = 'bin/release.py'
#回滚的脚本名称
ROLLBACKNAME = 'bin/rollback.py'
#检查备份包脚本名称
CHECKTARNAME = 'bin/checkTar.py'
#pptp拨号命令
PPTPCONNECTCMD = 'pptpsetup --create %s --server %s --username %s --password %s --encrypt --start'
PPTPCLOSECMD = 'pidof pptp | xargs kill'
PPTPROUTERADD = 'route add -net %s.0 netmask 255.255.255.0 dev ppp0'
PPTPROUTERDEL = 'route del -net %s.0 netmask 255.255.255.0'
