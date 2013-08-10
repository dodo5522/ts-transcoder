#!/usr/bin/python3

import os,sys,string,re

###################
# sub routine
###################
def GetListOfDirectoryToMove(RootDirectory=""):
	ListOfDirectoryToMove = [ \
			'/root/animal', \
			'/root/cinema', \
			'/root/dorama']
	return ListOfDirectoryToMove

def FindMediaFileWithKeyword(KeyWord=""):
	ListOfMediaFile = [ \
			"animalplanet.mp4", \
			"get_animal_in_fieald.mp4", \
			"some_animals.mp4"]
	return ListOfMediaFile

###################
# main routine
###################

try:
	ARGVS = sys.argv
	ARGC = len(ARGVS)
	OWN = ARGVS[0]
	
	ListOfDir = GetListOfDirectoryToMove(os.path.curdir)
	
	for Dir in ListOfDir:
		ListOfMediaFile = FindMediaFileWithKeyword(Dir)
		
		for MediaFile in ListOfMediaFile:
			print("Keyword is {KeyWord}, Mediafile is {KeyMediaFile}.".format(KeyWord=Dir, KeyMediaFile=MediaFile))

except Exception as err:
	print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))

