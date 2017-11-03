#!/usr/bin/env python3

""" Main script to demo CDNetworks APIs
    For specific API calls please see Browser.py and Base.py
    By Yegor Shrayev
"""

import json
from cdnetworks import Browser, Actions, Base, select_item_by_user
from pprint import pprint
from pprint import PrettyPrinter
import params
import getpass


def get_args():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description="Demo script for CDNetworks API", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--username", metavar='USERNAME', dest="username", help="CDNetworks Portal username")
    parser.add_argument("-p", "--password", metavar='PASSWORD', dest="password", help="CDNetworks Portal password")
    parser.add_argument("-g", "--svcGroupName", metavar='GROUPNAME', dest="svc_group_name",
                        help="CDNetworks Control Group Name")
    parser.add_argument("-sv", "--svcName", metavar='SERVICENAME', dest="svc_name",
                        help="CDNetworks Service Name")
    parser.add_argument("-s", "--srcPADName", metavar='SRCPAD', dest="src_pad_name",
                        help="PAD from which you clone or copy specific SAM rule")
    parser.add_argument("-a", "--action", metavar='ACTION', dest="action",
                        help="Choise one of follow actions (Browse, ClonePAD, CloneSAM)",
                        choices=['Browse', 'ClonePAD', 'CloneSAM'], default='Browse')
    parser.add_argument("-v", "--verbose", action="store_false", dest="verbose", help="Disable verbose messages")
    group = parser.add_argument_group('Clone PAD / Clone SAM rules arguments')
    group.add_argument("-d", "--destPADName", metavar='DESTPAD', dest="dest_pad_name",
                       help="PAD to where you clone or copy specific SAM rule."
                            " Required if ClonePAD or CloneSAM are set")
    group.add_argument('--origin', metavar='ORIGIN', dest="origin",
                       help="Specify origin in case it is different from sourse", default=None)
    group.add_argument("--description", metavar='DESTPAD', dest="description", help="New PAD description", default=None)

    args = parser.parse_args()
    if not args.username:
        if not params.username:
            args.username = input('Username:')
        else:
            args.username = params.username
    if not args.password:
        if not params.password:
            args.password = getpass.getpass('Password:')
        else:
            args.password = params.password
    if not args.svc_group_name and params.svc_group_name:
        args.svc_group_name = params.svc_group_name
    if not args.svc_name and params.svc_name:
        args.svc_name = params.svc_name
    if not args.src_pad_name and params.src_pad_name:
        args.src_pad_name = params.src_pad_name
    if not args.dest_pad_name and params.dest_pad_name:
        args.dest_pad_name = params.dest_pad_name
    if not args.dest_pad_name and params.dest_pad_name:
        args.dest_pad_name = params.dest_pad_name
    if args.action == 'ClonePAD':

        if not args.dest_pad_name:
            args.dest_pad_name = input('Please enter a name of new PAD:')

        if not args.origin and params.origin and params.origin != '#DONTASKUSER#':
            args.origin = params.origin
        if not args.origin and params.origin != '#DONTASKUSER#':
            args.origin = input(
                'Please enter origin for new PAD\n(Press Enter if you like to use origin from source PAD):')

        if not args.description and params.description and params.description != '#DONTASKUSER#':
            args.description = params.description
        if not args.description and params.description != '#DONTASKUSER#':
            args.description = input('Please enter description for new PAD:')

    return args


args = get_args()

base = Base(args.username, args.password, args.verbose)

auth_token = base.login()

browser = Browser(base)

# Select a control group and return sessionToken
sessionToken = browser.get_token_for_control_group(auth_token, args.svc_group_name)

# Select a PAD or service type and return API for it.
apiKey = browser.get_api_key_for_service(sessionToken, args.svc_name)

actions = Actions(base, sessionToken, apiKey)

# PAD can include referance to additional PADs, in such case one should be selected
PADsList = browser.get_pad_list(sessionToken, apiKey)

srcPADName = browser.select_pad(PADsList, args.src_pad_name)

if args.action == 'Browse' or args.action == 'CloneSAM':
    PADDetails = browser.get_pad(sessionToken, apiKey, srcPADName)
    PadSAM = browser.get_sam(sessionToken, apiKey, srcPADName)

if args.action == 'Browse':
    # Get PAD details and SAM info, output will be writen to file as it too long to show on screen.
    logFile = open(srcPADName + 'Details.' + base.APIFORMAT, 'w')
    pp = PrettyPrinter(indent=4, stream=logFile)
    pp.pprint(PADDetails)
    pprint("File name for PAD details is %s" % logFile.name)
    logFile = open(srcPADName + 'SAMRules.' + base.APIFORMAT, 'w')
    pp = PrettyPrinter(indent=4, stream=logFile)
    pp.pprint(PadSAM)
    pprint("File name for PAD SAM rules is %s" % logFile.name)

if args.action == 'ClonePAD':
    # To create new PAD Contact number is required
    seclectedContract = browser.get_contract_number(sessionToken, apiKey)
    pprint("Selected contract is: %s" % seclectedContract) if args.verbose else None
    output = actions.clone_pad(seclectedContract, srcPADName, args.destPADName, args.origin, args.description)
    pprint(output) if args.verbose else None

if args.action == 'CloneSAM':
    SAMRules = PadSAM['PadConfigResponse']['data']['data']['details']
    # Select Rule to clone
    ruleNum = select_item_by_user(SAMRules, False, 'name')
    # Select destanation PAD
    if not args.destPADName:
        args.destPADName = browser.select_pad(PADsList, args.dest_pad_name)
    # Will add CLONED tag incase source and destanation are the same PAD
    if args.destPADName == srcPADName:
        SAMRules[ruleNum]['name'] = 'CLONED ' + SAMRules[ruleNum]['name']
    # Select posision for new rule in destanation PAD and insert it
    DestPadSAM = browser.get_sam(sessionToken, apiKey, args.destPADName)
    DestPadSAMRules = DestPadSAM['PadConfigResponse']['data']['data']['details']
    AfterRuleNum = select_item_by_user(DestPadSAMRules, False, 'name')
    DestPadSAMRules.insert(AfterRuleNum, SAMRules[ruleNum])
    # Dump json and run API
    params_json = json.dumps(DestPadSAMRules)
    output = actions.add_sam_to_pad(args.destPADName, params_json)
    pprint(output) if args.verbose else None


#base.logout(sessionToken)
