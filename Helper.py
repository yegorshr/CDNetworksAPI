#!/usr/bin/env python3

"""	Library that includes functions that not directly use CDNetworks APIs\n
	By Yegor Shrayev
"""
import params
import getpass
from pprint import pprint


def selectItemByUser(List):

	NumberOfItems = len(List)
	IsItemSelected = 0
	if NumberOfItems == 0:
		raise ValueError('No items found in List') 
	if NumberOfItems == 1:
		IsItemSelected = 1
	if NumberOfItems > 1:
		pprint(List)

		while True:
			try:
				session = int(input('Please make a selection (1-%d): ' % NumberOfItems ))
				if session > NumberOfItems or session < 1:
					raise ValueError
				IsItemSelected = session
				break
			except ValueError:
				print ("'%s' is not a valid number." % session)
	
	return IsItemSelected-1


def get_args():
	from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
	parser = ArgumentParser(description="Demo script for CDNetworks API", formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument("-u","--username", 		metavar='USERNAME', 	dest="Username", 		help="CDNetworks Portal username")
	parser.add_argument("-p","--password", 		metavar='PASSWORD', 	dest="Password", 		help="CDNetworks Portal password")
	parser.add_argument("-g","--svcGroupName", 	metavar='GROUPNAME', 	dest="svcGroupName", 	help="CDNetworks Control Group Name")
	parser.add_argument("-s","--srcPADName", 	metavar='SRCPAD', 		dest="srcPADName", 		help="PAD from which you clone or copy specific SAM rule")
	parser.add_argument("-a","--action", 		metavar='ACTION', 		dest="action", 			help="Choise one of follow actions (Browse, ClonePAD, CloneSAM)", choices=['Browse', 'ClonePAD'], default = 'Browse') #, 'CloneSAM'
	parser.add_argument("-v","--verbose", 		action="store_false",	dest="verbose", 		help="Disable verbose messages" )
	group = parser.add_argument_group('Clone PAD / Clone SAM rules arguments')
	group.add_argument("-d","--destPADName", 	metavar='DESTPAD', 		dest="destPADName", 	help="PAD to where you clone or copy specific SAM rule. Required if ClonePAD or CloneSAM are set")
	group.add_argument('--origin', 				metavar='ORIGIN', 		dest="origin",			help="Specify origin in case it is different from sourse", default=None)
	group.add_argument("--description", 		metavar='DESTPAD', 		dest="description", 	help="New PAD description", default=None)


	args = parser.parse_args()
	if not args.Username:
		if not params.Username:
			args.Username = input('Username:')
		else: 
			args.Username = params.Username
	if not args.Password:
		if not params.Password:
			args.Password = getpass.getpass('Password:')
		else: 
			args.Password = params.Password
	if not args.svcGroupName and params.svcGroupName:
		args.svcGroupName = params.svcGroupName
	if not args.srcPADName and params.srcPADName:
		args.srcPADName = params.srcPADName
	if not args.destPADName and params.destPADName:
		args.destPADName = params.destPADName

	if args.action == 'ClonePAD':

		if not args.destPADName:
			args.destPADName = input('Please enter a name of new PAD:')

		if not args.origin and params.origin and params.origin != '#DONTASKUSER#':
			args.origin = params.origin
		if not args.origin and params.origin != '#DONTASKUSER#':
			args.origin = input('Please enter origin for new PAD\n(Press Enter if you like to use origin from source PAD):')

		if not args.description and params.description and params.description != '#DONTASKUSER#':
			args.description = params.description
		if not args.description and params.description != '#DONTASKUSER#':
			args.description = input('Please enter description for new PAD:')

	if args.action == 'CloneSAM':
		if not args.destPADName:
			args.destPADName = input('Please type a name of PAD where you like to copy SAM rule:')
	return args

def GetDictNumberInList(ListOfDict, LookForValue, message):
	IsFound = False
	count=-1
	for dict in ListOfDict:
		count+=1
		if (LookForValue in dict.values() ):
			IsFound = True
			break
	if not IsFound:
		raise ValueError (message)
	return count

def SelectedFromList(ListOfDict, LookForValue, message="Value not found" ):
	"""
		If Value set, get its dictonaty position.
		If not set ask user to select of list.
	"""
	if LookForValue:
		ChoosenSession = GetDictNumberInList(ListOfDict, LookForValue, message)
	else:
		ChoosenSession = selectItemByUser(ListOfDict)
	
	return ListOfDict[ChoosenSession]
