#!/usr/bin/env python3

"""	Main script to demo CDNetworks APIs
	For specific API calls please see Browser.py and Base.py
	By Yegor Shrayev
"""

import Helper
import json
from Browser import Browser
from Base import Base
import pprint as pp
from Actions import Actions
import logging

args = Helper.get_args()

base = Base(args)
actions = Actions(args)

#### LogIn ####
AutonticationToken = base.Login()

browser = Browser(args)

# Select a control group and return sessionToken
sessionToken = browser.GetTokenForSelectedControlGroup(AutonticationToken)

# Select a PAD or service type and return API for it.
apiKey = browser.GetAPIKeyForPAD(sessionToken)

# PAD can include referance to additional PADs, in such case one should be selected
PADsList = browser.GetPADsList(sessionToken, apiKey)

srcPADName = browser.SelectPAD(PADsList)

if args.action == 'Browse' or args.action == 'CloneSAM':

	# PAD can include referance to additional PADs, in such case one should be selected
	PADDetails = browser.GetPAD(sessionToken, apiKey ,srcPADName)
	PadSAM = browser.GetPADSam(sessionToken, apiKey ,srcPADName)

if args.action == 'Browse':
	# Get PAD details and SAM info, output will be writen to file as it too long to show on screen.
	logFile = open(srcPADName+'Details.'+base.APIFORMAT, 'w')
	ppFormat = pp.PrettyPrinter(indent=4, stream=logFile)
	logging.debug("PAD configuration:\n" + pp.pformat(PADDetails, indent=4))
	ppFormat.pprint(PADDetails)
	pp.pprint("File name for PAD details is %s" % logFile.name)
	logFile = open(srcPADName+'SAMRules.'+base.APIFORMAT, 'w')
	ppFormat = pp.PrettyPrinter(indent=4, stream=logFile)
	logging.debug("PAD SAM rules:\n" + pp.pformat(PadSAM, indent=4))
	ppFormat.pprint(PadSAM)
	pp.pprint("File name for PAD SAM rules is %s" % logFile.name)

if args.action == 'ClonePAD':
	#To create new PAD Contact number is required
	seclectedContract = browser.GetContractNomberForPAD(sessionToken, apiKey)
	logging.info("PAD SAM rules:\n" + pp.pformat(seclectedContract, indent=4))
	output = actions.ClonePAD(sessionToken, apiKey, seclectedContract, srcPADName, args.destPADName, args.origin, args.description)

if args.action == 'CloneSAM':
	SAMRules = PadSAM['PadConfigResponse']['data']['data']['details']
	#Select Rule to clone
	ruleNum = Helper.selectItemByUser(SAMRules, False, 'name')
	#Select destanation PAD
	if not args.destPADName:
		args.destPADName = browser.SelectPAD(PADsList)
	# Will add CLONED tag incase source and destanation are the same PAD
	if args.destPADName == srcPADName:
		SAMRules[ruleNum]['name'] = 'CLONED ' + SAMRules[ruleNum]['name']
	# Select posision for new rule in destanation PAD and insert it
	DestPadSAM = browser.GetPADSam(sessionToken, apiKey ,args.destPADName)
	DestPadSAMRules = DestPadSAM['PadConfigResponse']['data']['data']['details']
	AfterRuleNum = Helper.selectItemByUser(DestPadSAMRules, False, 'name')
	DestPadSAMRules.insert(AfterRuleNum,SAMRules[ruleNum])
	#Dump json and run API
	params_json = json.dumps(DestPadSAMRules)
	output = actions.AddSamToPAD( sessionToken, apiKey, args.destPADName,params_json )

base.Logout(sessionToken)