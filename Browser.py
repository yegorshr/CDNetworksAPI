#!/usr/bin/env python3

"""	#Browser.py is a demo script to use CDNetworks API to browse PADs' configurations \n
	By Yegor Shrayev
"""

from Base 	import Base
from Helper import selectItemByUser

class Browser(object):

	def __init__(self, args):
		self.args = args
		self.base = Base(args)

	def GetAPIKeyForPAD(self,sessionToken):
		"""
		Execute getApiKeyList, search for PAD/service APIKey.
		For new PAD you must to have service where type is 0.
		Unless you need to create new PAD, service Name will be as PAD Name
		
		Parameters
		----------
		sessionToken 	: Login token from GetTokenForSelectedControlGroup function.
		
		Returns
		-------
		Error http code or decoded json output
		"""
		#In case of implemention action to create new PAD, this login need to be modified
		params = {
			'sessionToken': sessionToken,
			'output':self.base.APIFORMAT }
			
		ApiKeyList = self.base.RunRestAPI('getApiKeyList',params)

		if self.args.srcPADName:
			count=0
			for value in ApiKeyList["apiKeyInfo"]["apiKeyInfoItem"]:
				count+=1
				if (value['serviceName']==self.args.srcPADName):
					ChoosenSession = count
			if not ChoosenSession:
				raise ValueError ("PAD Name was not found.")
		else:
			ChoosenSession = selectItemByUser(ApiKeyList["apiKeyInfo"]["apiKeyInfoItem"])

		return ApiKeyList["apiKeyInfo"]["apiKeyInfoItem"][ChoosenSession-1]['apiKey']

	def GetTokenForSelectedControlGroup(self, AutonticationToken):
		"""
			Select a control group and return sessionToken
		"""
		if self.args.svcGroupName:
			count=0
			for value in AutonticationToken["loginResponse"]["session"]:
				count+=1
				if (value['svcGroupName']==self.args.svcGroupName):
					ChoosenSession = count
			if not ChoosenSession:
				raise ValueError ("Group Name was not found.")
		else:
			ChoosenSession = selectItemByUser(AutonticationToken["loginResponse"]["session"])
		
		return AutonticationToken["loginResponse"]["session"][ChoosenSession-1]["sessionToken"]

	def GetPADsList(self, sessionToken, apiKey):

		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'output': self.base.APIFORMAT }
		return self.base.RunRestAPI('pan/site/list',params)

	def SelectPAD (self,PADsList):
		if self.args.srcPADName:
			count=0
			for value in PADsList["PadConfigResponse"]["data"]["data"]:
				count+=1
				if (value['pad']==self.args.srcPADName):
					ChoosenSession = count
			if not ChoosenSession:
				raise ValueError ("Group Name was not found.")
		else:
			ChoosenSession = selectItemByUser(PADsList["PadConfigResponse"]["data"]["data"])
		
		return PADsList["PadConfigResponse"]["data"]["data"][ChoosenSession-1]["pad"]

	def GetPAD(self, sessionToken, apiKey, padName, prod=True):
		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'pad' : padName,
			'prod' : prod,
			'output': self.base.APIFORMAT }
		return self.base.RunRestAPI('pan/site/view',params)

	def GetPADSam(self, sessionToken, apiKey, PADName):

		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'output': self.base.APIFORMAT }
		return self.base.RunRestAPI('pan/sam/'+ PADName + '/view',params)


