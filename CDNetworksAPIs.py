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
from Actions import Actions

args = Helper.get_args()

base = Base(args)
actions = Actions(args)

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

if args.action == 'Browse':

	# PAD can include referance to additional PADs, in such case one should be selected
	PADDetails = browser.GetPAD(sessionToken, APIKey ,srcPADName)
	PadSAM = browser.GetPADSam(sessionToken, APIKey ,srcPADName)
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
	seclectedContract = browser.GetContractNomberForPAD(sessionToken, APIKey)
	pprint("Selected contract is: %s" % seclectedContract) if args.verbose else None
	output = actions.ClonePAD(sessionToken, APIKey, seclectedContract, srcPADName, args.destPADName, args.origin, args.description)
	pprint(output) if args.verbose else None

base.Logout(sessionToken)