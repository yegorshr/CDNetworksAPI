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
	
	def GetDictNumberInList(self, ListOfDict, LookForValue, message):
		count=-1
		for dict in ListOfDict:
			count+=1
			if (LookForValue in dict.values() ):
				IsFound = True
				break
		if not IsFound:
			raise ValueError (message)
		return count
	
	def SelectedFromList(self, ListOfDict, LookForValue, message="Value not found" ):
		"""
			If Value set, get its dictonaty position.
			If not set ask user to select of list.
		"""
		if LookForValue:
			ChoosenSession = self.GetDictNumberInList(ListOfDict, LookForValue, message)
		else:
			ChoosenSession = selectItemByUser(ListOfDict)
		
		return ListOfDict[ChoosenSession]

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
		
		Dict = self.SelectedFromList(ApiKeyList["apiKeyInfo"]["apiKeyInfoItem"], self.args.srcPADName, "PAD Name was not found.")
		return Dict['apiKey']

	def GetTokenForSelectedControlGroup(self, AutonticationToken):
		"""
			Select a control group and return sessionToken
		"""
		Dict = self.SelectedFromList(AutonticationToken["loginResponse"]["session"], self.args.svcGroupName, "Group Name was not found.")
		return Dict['sessionToken']

	def GetPADsList(self, sessionToken, apiKey):

		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'output': self.base.APIFORMAT }
		return self.base.RunRestAPI('pan/site/list',params)

	def SelectPAD (self,PADsList):
		Dict = self.SelectedFromList(PADsList["PadConfigResponse"]["data"]["data"], self.args.srcPADName, "PAD Name was not found.")
		return Dict["pad"]

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

	def GetContractNomberForPAD(self,sessionToken, apiKey):
		params = {
			'sessionToken': sessionToken,
			'apiKey': apiKey,
			'output': self.base.APIFORMAT }
			
		ContractList = self.base.RunRestAPI('pan/contract/list',params)
		ChoosenSession = selectItemByUser(ContractList['PadConfigResponse']['data']['data'])
		ContractNumber = ContractList['PadConfigResponse']['data']['data'][ChoosenSession]['contract_no']
		return ContractNumber
