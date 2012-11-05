#/bin/env python
#-*-coding:utf-8-*-
import web
from conf import config
import json
import time
from modules import dbHelp
from modules import valids
from modules import vcs
from modules import vcspack
import math
import hashlib
import os
from modules import serlink

urls = (
		'', 'ReProject',
        '/',  'Project',
		'/create/', 'Create',
		'/change/', 'Change',
		'/update/', 'Update',
		'/shortlist/', 'ShortList',
		'/vcslist/', 'VcsList',
		'/package/', 'Package',
		'/packlist/(.+)/(\d*)', 'PackList',
		'/packdetail/(\d+)', 'PackDetail',
		'/packstatus/(\d+)/(\d+)', 'PackStatus',
		'/actioning/(\d+)/(.+)', 'Actioning',
		'/rollbacking/(\d+)/(.+)', 'Rollbacking',
        )

#def onload(handler):
#	try:
#		web.ctx.session.uName is None
#	except:
#		if 'HTTP_X_REQUESTED_WITH' in web.ctx.environ and web.ctx.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
#			return json.dumps({'res' : 'error', 'msg' : '您已经退出登录，请<a href="/index?login">重新登录</a>'})
#		else:
#			web.seeother('/index?login', True)
#
#	return handler()

render = config.render
appProject = web.application(urls, globals())
#appProject.add_processor(onload)

class ReProject(object):
	def GET(self): raise web.redirect('/')

class Project(object):
    def GET(self):
		'''取数据库项目信息'''
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			plist = db.select('c2_project', order='p_status asc, p_cdateline desc')
			if len(plist) == 0:
				plist = ''
			#return render.project(plist = plist, ac = 2, logUserInfo = web.ctx.session)
			return render.project(plist = plist)
		except:
			#return render.project(ac = 2, logUserInfo = web.ctx.session)
			return render.project(ac = 2)


class Create(object):
	def POST(self):
		inputs = web.input()
		name = inputs['pname'].strip()
		vcspath = inputs['vcs'].strip()
		vcsuser = inputs['vcsuser'].strip()
		vcspass = inputs['vcspass'].strip()
		v = valids.Valids()

		if v.isEmpty(name) or \
			v.isEmpty(vcspath) or \
			v.isEmpty(vcsuser) or \
			v.isEmpty(vcspass):
			return json.dumps({'res' : 0, 'msg' : '各项不能为空'})

		if vcspath[-1] == '/':
			vcspath = vcspath[0:-1]

		#入库操作
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.insert('c2_project', p_name = name, \
			p_vcspath = vcspath, \
			p_user = vcsuser, \
			p_pass = vcspass, \
			p_cdateline = time.time(), \
			p_status = 1)

			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Change(object):
	def POST(self):
		inputs = web.input()
		status = 1
		if len(inputs['checkboxs']) == 0:
			return json.dumps({'res' : 0, 'msg' : '请至少选择一项'})

		if len(inputs['status']) > 0:
			status = inputs['status'].strip()

		#修改数据库
		try:
			ids = inputs['checkboxs'].strip().split('|')
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_project', p_status = status, where = 'p_id IN $ids', vars=locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class Update(object):
	def POST(self):
		inputs = web.input()
		name = inputs['name'].strip()
		id = inputs['id'].strip()
		val = inputs['val'].strip()
		v = valids.Valids()

		if v.isEmpty(name) or \
			v.isEmpty(id) or \
			v.isEmpty(val):
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#修改数据
		try:
			if name == 'vcs':
				if val[-1] == '/':
					val = val[0:-1]
				dVal = {'p_vcspath' : val}
			elif name == 'vcsuser':
				dVal = {'p_user' : val}
			elif name == 'vcspass':
				dVal = {'p_pass': val}
			else:
				return json.dumps({'res' : 0, 'msg' : '数据不合法'})

			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_project', where = 'p_id = $id', vars = locals(), **dVal)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统错误'})

class VcsList(object):
	def POST(self):
		inputs = web.input()
		vids = inputs['vids'].strip()
		pro = inputs['pro'].strip()
		v = valids.Valids()
		if v.isEmpty(vids) or v.isEmpty(pro):
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		try:
			vidsArr = [int(x) for x in vids.split('|')]
		except:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		vidsArr.sort(reverse = True)

		#查找项目信息
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			res = db.select('c2_project', what = 'p_vcspath, p_user, p_pass', where = 'p_id = $pro AND p_status = 1', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无项目信息'})

			rs = res[0]
			pv = vcs.Vcs(vPath = rs.p_vcspath, vUser = rs.p_user, vPass = rs.p_pass)

			data={'res' : 1, 'logs' : pv.getLog(vidsArr),'lastVersion':''}
			vrs = db.select('c2_revision', what = 'r_id, r_no', where = 'p_id = $pro', limit = '1', order = 'r_id DESC', vars = locals())
			if len(vrs) != 0:
				data['lastVersion']=vrs[0].r_no
			return json.dumps(data)
		except Exception, e:
#return json.dumps({'res' : 0, 'msg' : '版本号错误'})
			return json.dumps({'res' : 0, 'msg' : e.args})

class Package(object):
	def POST(self):
		inputs = web.input()
		pro = inputs['pro'].strip()
		vals = inputs['vals'].strip()
		verno = inputs['verno'].strip()
		v = valids.Valids()
		if v.isEmpty(pro) or v.isEmpty(vals) or v.isEmpty(verno):
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#插入最新的版本信息并得到该版本对应id
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看项目id是否存在
			res = db.select('c2_project', what = 'p_vcspath, p_user, p_pass', where = 'p_id = $pro AND p_status = 1', limit = '1', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '该项目不存在或者状态不可用'})

			#查看该版本号是否存在
			rNos = db.select('c2_revision', what = '*', where = 'r_no = $verno', vars = locals())
			if len(rNos) > 0:
				return json.dumps({'res' : 0, 'msg' : '该版本号已经存在'})

			rId = db.insert('c2_revision', p_id = pro, \
			r_no = verno, r_cdateline = time.time(), \
			r_status = 1)
			if rId < 1:
				return json.dumps({'res' : 0, 'msg' : '数据库出错'})

			#拆分字符串
			valsArr = vals.split('|')
			valsNum = len(valsArr)
			insValTmp = [dict(zip(['f_ver', 'f_action', 'f_path'], x.split('::'))) for x in valsArr]
			insValTmp.sort()
			insVal = []
			packVal = []
			for x in insValTmp:
				x.update({'r_id' : rId})
				insVal.append(x)
				if x['f_action'] != 'D':
					packVal.append(x)

			#插入数据库
			rs = db.multiple_insert('c2_files', insVal)
			if len(rs) != valsNum:
				return json.dumps({'res' : 0, 'msg' : '打包出错，请重试'})

			#真正实际打包到相应位置
			r = res[0]
			vcsPack = vcspack.VcsPack(vpath = r.p_vcspath, vuser = r.p_user, vpass = r.p_pass, vid = pro)
			vcsPack.goPack(packVal, verno)
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '系统出错'})

class PackList(object):
	def GET(self, pro, page = None):
		v = valids.Valids()
		if v.isEmpty(pro) or int(pro) == 0:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		if page == '':
			page = 1

		page = int(page)

		eachPage = 10
		#查找数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看项目id是否存在
			res = db.select('c2_project', what = 'p_id', where = 'p_id = $pro AND p_status = 1', limit = '1', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '该项目不存在或者状态不可用'})

			#查看打包总数
			ct = db.select('c2_revision', what = 'COUNT(*) AS c', where = 'p_id = $pro', vars = locals())
			allNums = ct[0].c
			if allNums <= 0: 
				return json.dumps({'res' : 0, 'msg' : '暂无已经打包的列表'})

			#最大页数
			maxPage = int(math.ceil(float(allNums)/eachPage))
			if page > maxPage:
				page = maxPage

			#查看该项目下的打包记录
			rs = db.select('c2_revision', what = 'r_id, r_no, s_id, s_name, r_dateline, r_cdateline, r_status', where = 'p_id = $pro', limit = '%d, %d' % ((page-1)*eachPage, eachPage), order = 'r_id DESC', vars = locals())
			if len(rs) == 0:
				return json.dumps({'res' : 0, 'msg' : '已经没有数据了'})

			return json.dumps({'res' : 1, 'list' : [r for r in rs], 'maxPage' : maxPage})
		except:
			return json.dumps({'res' : 0, 'msg' : '读取失败，请刷新'})

class PackDetail(object):
	def GET(self, rId):
		v = valids.Valids();
		if v.isEmpty(rId) or int(rId) == 0:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#查找数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			#查看项目id是否存在
			res = db.select('c2_files', what = 'f_ver, f_path', where = 'r_id = $rId', vars = locals())
			if len(res) == 0:
				return json.dumps({'res' : 0, 'msg' : '该版本没有包含任何文件'})

			return json.dumps({'res' : 1, 'list' : [r for r in res]})
		except:
			return json.dumps({'res' : 0, 'msg' : '读取失败，请刷新'})

class PackStatus(object):
	def GET(self, rSt, rId):
		v = valids.Valids()
		if v.isEmpty(rId) or int(rId) == 0 or v.isEmpty(rSt) or int(rSt) == 0 or int(rSt) not in [1, 2]:
			return json.dumps({'res' : 0, 'msg' : '数据不合法'})

		#更新数据库
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			db.update('c2_revision', r_status = rSt, where = 'r_id = $rId', vars = locals())
			return json.dumps({'res' : 1})
		except:
			return json.dumps({'res' : 0, 'msg' : '删除失败'})

class ShortList(object):
	def GET(self):
		'''取数据库项目信息'''
		try:
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			plist = db.select('c2_project', what = 'p_id, p_name', where = 'p_status = 1', order='p_cdateline desc')
			if len(plist) == 0:
				return json.dumps({'res' : 0, 'msg' : '暂无项目，请先创建项目'})

			return json.dumps({'res' : 1, 'list' : [l for l in plist]})
		except:
			return json.dumps({'res' : 0, 'msg' : '项目列表读取失败'})

class Actioning(object):
	def GET(self, serId, packageId):
		web.header('Content-type', 'text/html;charset=UTF-8')
		web.header("Cache-Control", "no-cache, must-revalidate")
		web.header("Expires", "Mon, 26 Jul 1997 05:00:00 GMT")
		yield '<style>body{font-size:14px}</style>'
		v = valids.Valids()
		pkId = packageId.strip()
		sId = serId.strip()
		if v.isEmpty(pkId) or v.isEmpty(sId):
			yield '<div>请选择要发布或回滚的版本包和对应的目标服务器，并点击右上角的X重新发布</div>'
			return

		try:
			#取的目标服务器信息和对应的项目id
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			sInfo = db.select('c2_server', what = '*', where = 's_id = $sId AND s_status = 1', limit = 1, vars = locals())
			if len(sInfo) == 0:
				yield '<div>选择的服务器被关闭或者不存在</div>'
				return

			#查看项目信息看项目是否可用
			serInfo = dict(sInfo[0])
			proId = serInfo['p_id']
			proInfo = db.select('c2_project', what = '*', where = 'p_id = $proId AND p_status = 1', limit = 1, vars = locals())
			if len(proInfo) == 0:
				yield '<div>对应的项目不可用，请检查项目状态</div>'

			projectInfo = dict(proInfo[0])

			packDir = config.PACKAGEROOT % (hashlib.new('md5', str(serInfo['p_id'])).hexdigest()[8 : -8])
			ids = pkId.split('|')
			##查看包id对应的项目id是否正确
			pInfo = db.select('c2_revision', what = 'r_id, r_no', where = 'r_status <> 2 AND r_id IN $ids', order = 'r_id ASC', vars = locals())
			if len(pInfo) != len(ids):
				yield '<div>发布包数量不正确，请点击右上角的X重新选择发布</div>'
				return

			#发布开始
			#判断包是否都已经存在，不存在则从数据库读取重新打包
			yield '<div>检测发布包状态...</div>'
			rePack = []
			packInfo = [dict(p) for p in pInfo]
			vPack = vcspack.VcsPack(vpath = projectInfo['p_vcspath'], vuser = projectInfo['p_user'], vpass = projectInfo['p_pass'], vid = proId)
			for p in packInfo:
				if os.path.isfile(packDir + '%s.tar.gz' % p['r_no']) is False:
					rePack.append([p['r_id'], p['r_no']])
					yield ('<div style="color:#f30">检测到<b>%s</b>版本发布包不正常，将重新打包...</div>' % str(p['r_no']))
					#重新打包
					yield ('<div>正在重新打包...</div>')
					#重新从数据库读取打包列表
					rId = p['r_id']
					pkList = db.select('c2_files', what = 'f_action, f_path, f_ver', where = 'r_id = $rId AND f_action != "D"', order = 'f_ver ASC', vars = locals())
					if len(pkList) == 0:
						yield ('<div style="color:#f30">该版本不存在打包文件，将放弃重新打包</div>')
						continue

					vPack.goPack([{'f_path' : vers.f_path, 'f_action' : vers.f_action, 'f_ver' : vers.f_ver} for vers in pkList], p['r_no'])
					yield ('<div style="color:#86cc12"><b>%s</b>重新打包完毕...</div>' % str(p['r_no']))
				else:
					yield ('<div style="color:#86cc12"><b>%s</b>版本发布包正常</div>' % str(p['r_no']))

			try:
				sl = serlink.SerLink(host = serInfo['s_host'], user = serInfo['s_user'], pw = serInfo['s_pass'], bdir = serInfo['s_bdir'], pdir = serInfo['s_pdir'])
				isVpn = (v.isEmpty(serInfo['s_vpn']) == False) and (v.isEmpty(serInfo['s_vpnuser']) == False) and (v.isEmpty(serInfo['s_vpnpass']) == False)
				if isVpn:
					yield '<div>开始拨号连接...</div>'
					vpnRs = sl.vpnConnect({'vpn' : serInfo['s_vpn'], 'user' : serInfo['s_vpnuser'], 'pw' : serInfo['s_vpnpass'], 'type' : serInfo['s_vpnpro'], 'route' : serInfo['s_host']})
					yield '<div>%s</div>' % str(vpnRs)
					if vpnRs.find('succeeded') == -1:
						yield '<div style="color:#f30">vpn拨号失败，请重试</div>'
						return

				#拷贝包文件到目标服务器
				yield '<div>拷贝包文件到目标服务器<b>%s</b>...</div>' % str(serInfo['s_host'])
				scpRs = sl.scpSend([packDir + '%s.tar.gz' % p['r_no'] for p in packInfo])
				if scpRs.find('ERROR') != -1:
					yield '<div style="color:#f30">发布包上传失败，请联系管理员</div>'
					if isVpn:
						sl.vpnClose()
						yield 'vpn关闭'
					return

				yield '<div style="color:#86cc12">发布包上传成功</div>'
				yield '<div>开始在目标服务器操作...</div>'
				relRs = sl.sshRelese([p['r_no'] for p in packInfo])
				yield '<div style="color:f30">%s</div>' % str(relRs)
				#没有错误和失败则更新版本包状态为已发布
				if relRs.find('[ERROR]') == -1:
					ids = [p['r_id'] for p in packInfo]
					db.update('c2_revision', r_dateline = time.time(), r_status = 3, s_id = serInfo['s_id'], s_name = serInfo['s_name'], where = 'r_id IN $ids AND r_status <> 2', vars=locals())
					db.multiple_insert('c2_log', [{'s_id' : serInfo['s_id'], 's_name' : serInfo['s_name'], 'r_id' : p['r_id'], 'r_no' : p['r_no'], 'r_dateline' : time.time()} for p in packInfo])
				
				if isVpn:
					#关闭vpn链接
					sl.vpnClose()
					yield 'vpn关闭'
			except Exception, e:
				yield '<div style="color:#f30">' + str(e) + '</div>'
				return 
		except Exception, e:
			yield '服务器故障，请点击右上角的X重新发布'

class Rollbacking(object):
	def GET(self, serId, packageId):
		web.header('Content-type', 'text/html;charset=UTF-8')
		web.header("Cache-Control", "no-cache, must-revalidate")
		web.header("Expires", "Mon, 26 Jul 1997 05:00:00 GMT")
		yield '<style>body{font-size:14px}</style>'
		v = valids.Valids()
		pkId = packageId.strip()
		sId = serId.strip()
		if v.isEmpty(pkId) or v.isEmpty(sId):
			yield '<div>请选择要发布或回滚的版本包和对应的目标服务器，并点击右上角的X重新发布</div>'
			return

		try:
			#取的目标服务器信息和对应的项目id
			dbase = dbHelp.DbHelp()
			db = dbase.database()
			sInfo = db.select('c2_server', what = '*', where = 's_id = $sId AND s_status = 1', limit = 1, vars = locals())
			if len(sInfo) == 0:
				yield '<div>选择的服务器被关闭或者不存在</div>'
				return

			#查看项目信息看项目是否可用
			serInfo = dict(sInfo[0])
			proId = serInfo['p_id']
			proInfo = db.select('c2_project', what = '*', where = 'p_id = $proId AND p_status = 1', limit = 1, vars = locals())
			if len(proInfo) == 0:
				yield '<div>对应的项目不可用，请检查项目状态</div>'

			projectInfo = dict(proInfo[0])

			packDir = config.PACKAGEROOT % (hashlib.new('md5', str(serInfo['p_id'])).hexdigest()[8 : -8])
			ids = pkId.split('|')
			##查看包id对应的项目id是否正确
			pInfo = db.select('c2_revision', what = 'r_id, r_no', where = 'r_status <> 2 AND r_id IN $ids', order = 'r_id DESC', vars = locals())
			if len(pInfo) != len(ids):
				yield '<div>回滚包数量不正确，请点击右上角的X重新选择发布</div>'
				return

			#回滚开始
			packInfo = [dict(p) for p in pInfo]
			try:
				sl = serlink.SerLink(host = serInfo['s_host'], user = serInfo['s_user'], pw = serInfo['s_pass'], bdir = serInfo['s_bdir'], pdir = serInfo['s_pdir'])
				isVpn = (v.isEmpty(serInfo['s_vpn']) == False) and (v.isEmpty(serInfo['s_vpnuser']) == False) and (v.isEmpty(serInfo['s_vpnpass']) == False)
				if isVpn:
					yield '<div>开始拨号连接...</div>'
					vpnRs = sl.vpnConnect({'vpn' : serInfo['s_vpn'], 'user' : serInfo['s_vpnuser'], 'pw' : serInfo['s_vpnpass'], 'type' : serInfo['s_vpnpro'], 'route' : serInfo['s_host']})
					yield '<div>%s</div>' % str(vpnRs)
					if vpnRs.find('succeeded') == -1:
						yield '<div style="color:#f30">vpn拨号失败，请重试</div>'
						return

				pNos = [p['r_no'] for p in packInfo]

				yield '<div>检测回滚包是否存在</div>'
				checkTar = sl.checkTar(pNos)
				yield '<div style="color:f30">%s</div>' % str(checkTar)
				if checkTar.find('[ERROR]') > 0:
					yield '<div style="color:#f30">回滚失败，服务器上的备份包缺失，请检查</div>'
					return

				yield '<div>开始在目标服务器进行回滚操作...</div>'
				relRs = sl.sshRollback(pNos)
				yield '<div style="color:f30">%s</div>' % str(relRs)
				#没有错误和失败则更新版本包状态为已发布
				if relRs.find('[ERROR]') == -1:
					ids = [p['r_id'] for p in packInfo]
					db.update('c2_revision', r_dateline = time.time(), r_status = 4, s_id = serInfo['s_id'], s_name = serInfo['s_name'], where = 'r_id IN $ids AND r_status <> 2', vars=locals())
					db.multiple_insert('c2_log', [{'s_id' : serInfo['s_id'], 's_name' : serInfo['s_name'], 'r_id' : p['r_id'], 'r_no' : p['r_no'], 'r_dateline' : time.time()} for p in packInfo])
				
				if isVpn:
					#关闭vpn链接
					sl.vpnClose()
					yield 'vpn关闭'
			except Exception, e:
				yield '<div style="color:#f30">' + str(e) + '</div>'
				return 
		except Exception, e:
			yield '服务器故障，请点击右上角的X重新发布'
