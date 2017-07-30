#Actions.py
from Base import Base

class Actions(object):

	def __init__(self, args):
		self.args = args
		self.base = Base(args)

	def CreatePAD (sessionToken, apiKey, contractNumber, newPADName, origin,description=None):
		params = {
			'sessionToken': sessionToken,
			'apiKey' : apiKey,
			'pad' : newPADName,
			'product' : contractNumber,
			'origin' : origin,
			'description': description,
			'output': self.base.APIFORMAT }

		return self.base.RunRestAPI('pan/site/v2/add',params)

	def ClonePAD (self,sessionToken, apiKey, contractNumber, srcPadName, newPADName, origin=None,description=None):
		params = {
			'sessionToken'	: sessionToken,
			'apiKey' 		: apiKey,
			'pad' 			: newPADName,
			'product' 		: contractNumber,
			'copy_settings_from': srcPadName,
			'output'		: self.base.APIFORMAT }
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
