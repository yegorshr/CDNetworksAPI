#!/usr/bin/env python3

"""	Base.py includes functions to demo CDNetworks APIs functionality such as login and API execution\n
	By Yegor Shrayev
"""
import requests
import json
from pprint import pprint
from pprint import PrettyPrinter

class Base(object):

	def __init__(self, args):
		self.args = args


	API_URL = "https://openapi.cdnetworks.com/api/rest/" # CDNetworks API url 
	APIFORMAT = "json" # API output format

	def RunRestAPI(self,APIName, parameters):
		"""
		Execute Rest API
		
		Parameters
		----------
		APIName 	: API name Example "login" or "pan/contract/list"
		parameters 	: dictionary of paramenter for API

		Returns
		-------
		Error http code or decoded json output
		"""
		fullURL = self.API_URL + APIName
		response = requests.get(url=fullURL,params=parameters, verify=True)
		print ('Executed url is %s' % (response.url)) 							if self.args.verbose else None
		print ('Return Code for %s is %s' % (APIName, response.status_code)) 	if self.args.verbose else None
		
		# On success, response code will be 200
		if(response.ok):
			# Loading the response data and decode as response not in utf-8 and has digits
			output = json.loads(response.content.decode('utf-8'))
			return output
		else:
			# If response code is not ok (200), print the resulting error
			response.raise_for_status()

	def Login(self):
		params = {
			'user': self.args.Username,
			'pass': self.args.Password,
			'output': self.APIFORMAT }
		output = self.RunRestAPI('login',params)
		if output['loginResponse']['resultCode'] == 101:
			raise ValueError("User login information is incorrect")
		pprint (output) if self.args.verbose else None
		return output

	def Logout(self,sessionToken):
		params = {
			'sessionToken':sessionToken,
			'output': self.APIFORMAT }
		output = self.RunRestAPI('logout',params)
		pprint(output) if self.args.verbose else None
