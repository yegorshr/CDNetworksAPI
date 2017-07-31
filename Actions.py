#!/usr/bin/env python3

"""	Library that includes functions that perform changes on CDNetworks configuration\n
	By Yegor Shrayev
"""
from Base import Base

class Actions(object):

	def __init__(self, args):
		self.args = args
		self.base = Base(args)

	def CreatePAD (self,sessionToken, apiKey, contractNumber, newPADName, origin,description=None):
		self.ClonePAD(sessionToken, apiKey, contractNumber, newPADName, origin, description)

	def ClonePAD (self,sessionToken, apiKey, contractNumber, srcPadName=None, newPADName='www.newPADName.com', origin=None,description=None):
		params = {
			'sessionToken'	: sessionToken,
			'apiKey' 		: apiKey,
			'pad' 			: newPADName,
			'product' 		: contractNumber,
			'output'		: self.base.APIFORMAT }
		if srcPadName:
			params['copy_settings_from'] = srcPadName
		if origin:
			params['origin'] = origin
		if description:
			params['description'] = description,
		return self.base.RunRestAPI('pan/site/v2/add',params)

	def AddSamToPAD(self, sessionToken, apiKey, destPADName, rule):
		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'sam_json' : rule,
			'output': self.base.APIFORMAT }
		return self.base.RunRestAPI('pan/sam/'+ destPADName + '/add',params)
