#!/usr/bin/env python
#-*-coding=utf-8-*-
import types
import re

class Valids:
	def __init__(self):
		pass

	def isNum(self, var):
		'''判断是否为整数'''
		return type(var) is types.IntType

	def isString(self, var):
		'''判断是否为字符串'''
		return type(var) is types.StringType

	def isFloat(self, var):
		'''判断是否为浮点数'''
		return type(var) is types.FloatType

	def isDict(self, var):
		'''判断是否为字典'''
		return type(var) is types.DictType

	def isTuple(self, var):
		'''判断是否为元组'''
		return type(var) is type.TupleType

	def isList(self, var):
		'''判断是否为列表'''
		return type(var) is type.ListType

	def isBoolean(self, var):
		'''判断是否为布尔值'''
		return type(var) is types.BooleanType

	def isEmpty(self, var):
		'''判断是否为空'''
		if len(var) == 0:
			return True
		return False
	
	def isNone(self, var):
		'''判断是否为None'''
		return type(var) is types.NoneType

	def isDate(self, var):
		'''判断是否是日期格式'''
		if len(var) == 10:
				rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
				if re.match(rule, var):
					return True

		return False

	def isEmail(self, var):
		'''判断是否email'''
		if re.match('[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', var):
			return True

		return False

	def isChineseCharString(self, var):
		'''判断是否中文字符串'''
		for x in var:
			if (x >= u"\u4e00" and x <= u"\u9fa5") or \
				(x >= u"\u0041" and x <= u"\u005a") or \
				(x >= u"\u0061" and x <= u"\u007a"):
				continue
			else:
				return False

		return True

	def isChineseChar(self, var):
		'''判断是否中文字符'''
		if var[0] > chr(127):
			return True

		return False


	def isIpAddr(self, var):
		'''判断ip格式'''
		if re.match('\d+\.\d+\.\d+\.\d+', var):
			return True

		return False
