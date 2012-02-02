from conf import config
import web

class DbHelp(object):
	def __init__(self):
		self.dbInfo = config.DBINFO

	def database(self):
		return web.database(
			dbn = self.dbInfo['dbn'], 
			db = self.dbInfo['db'],
			user = self.dbInfo['user'],
			pw = self.dbInfo['pw'],
			host = self.dbInfo['host']
		)
