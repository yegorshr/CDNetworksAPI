#!/usr/bin/env python3

"""	Main script to demo CDNetworks APIs
	For specific API calls please see Browser.py and Base.py
	By Yegor Shrayev
"""

import Helper
from Browser import Browser
from Base import Base
from pprint import pprint
from pprint import PrettyPrinter

args = Helper.get_args()

base = Base(args)

#### LogIn ####
AutonticationToken = base.Login()

browser = Browser(args)

# Select a control group and return sessionToken
sessionToken = browser.GetTokenForSelectedControlGroup(AutonticationToken)

# Select a PAD or service type and return API for it.
APIKey = browser.GetAPIKeyForPAD(sessionToken)

# PAD can include referance to additional PADs, in such case one should be selected
PADsList = browser.GetPADsList(sessionToken, APIKey)
srcPADName = browser.SelectPAD(PADsList)

# PAD can include referance to additional PADs, in such case one should be selected
PADDetails = browser.GetPAD(sessionToken, APIKey ,srcPADName)
PadSAM = browser.GetPADSam(sessionToken, APIKey ,srcPADName)

if args.action == 'Browse':
	# Get PAD details and SAM info, output will be writen to file as it too long to show on screen.
	logFile = open(srcPADName+'Details.'+base.APIFORMAT, 'w')
	pp = PrettyPrinter(indent=4, stream=logFile)
	pp.pprint(PADDetails)
	pprint("File name for PAD details is %s" % logFile.name)
	logFile = open(srcPADName+'SAMRules.'+base.APIFORMAT, 'w')
	pp = PrettyPrinter(indent=4, stream=logFile)
	pp.pprint(PadSAM)
	pprint("File name for PAD SAM rules is %s" % logFile.name)

if args.action == 'ClonePAD':
	params = {
		'sessionToken': sessionToken,
		'apiKey': APIKey,
		'output': base.APIFORMAT }
		
	ContractList = base.RunRestAPI('pan/contract/list',params)
	pprint(ContractList['PadConfigResponse']['data']['data'])
	#ContractNumber = ContractList['PadConfigResponse']['data']['data'][0]['contract_no']
	#pprint (CreatePAD(sessionToken, APIKey, ContractNumber,'Test1.deleteme.com','www.ptupload.com','Please delete me'))

base.Logout(sessionToken)