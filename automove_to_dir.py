#!/usr/bin/python3

import os,sys,string

ARGVS = sys.argv
ARGC = len(ARGVS)
OWN = ARGVS[0]

###################
# sub routine
###################
def GetListOfDirectoryToMove(RootDirectory=""):
	ListOfDirectoryToMove = ['test1', 'test2', 'test3']
	return ListOfDirectoryToMove


###################
# main routine
###################

try:
	print("test")
	ListOfDir = GetListOfDirectoryToMove(os.path.curdir)
	for Dir in ListOfDir:
		print(Dir)

except Exception as err:
	print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))
