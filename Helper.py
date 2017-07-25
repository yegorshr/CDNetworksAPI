#!/usr/bin/env python3

"""	Library that includes functions that not directly use CDNetworks APIs\n
	By Yegor Shrayev
"""
import params
import getpass
from argparse import ArgumentParser
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
	
	return IsItemSelected

def get_args():
	from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
	parser = ArgumentParser(description="Demo script for CDNetworks API", formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument("-u","--username", 		metavar='USERNAME', 	dest="Username", 		help="CDNetworks Portal username")
	parser.add_argument("-p","--password", 		metavar='PASSWORD', 	dest="Password", 		help="CDNetworks Portal password")
	parser.add_argument("-g","--svcGroupName", 	metavar='GROUPNAME', 	dest="svcGroupName", 	help="CDNetworks Control Group Name")
	parser.add_argument("-s","--srcPADName", 	metavar='SRCPAD', 		dest="srcPADName", 		help="PAD from which you clone or copy specific SAM rule")
	parser.add_argument("-d","--destPADName", 	metavar='DESTPAD', 		dest="destPADName", 	help="PAD to where you clone or copy specific SAM rule")
	parser.add_argument("-v","--verbose", 		action="store_false",	dest="verbose", 		help="Disable verbose messages" )
	
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
	return args
