#!/usr/bin/python3

import os,sys,string,re

###################
# sub routine
###################
def GetListOfDirectoryToMove(RootDirectory=""):
	print("Found directory:")

	DictOfDirectoryToMove = {}
	for FileOrDir in os.listdir(RootDirectory):
		if os.path.isdir(os.path.join(RootDirectory, FileOrDir)):
			print(" {Dir}".format(Dir=FileOrDir))
			DictOfDirectoryToMove[FileOrDir] = os.path.join(RootDirectory, FileOrDir)
	
	return DictOfDirectoryToMove

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
	DIR_MEDIA = ARGVS[1]
	DIR_TARGET = ARGVS[2]
	
	DictOfDir = GetListOfDirectoryToMove(DIR_TARGET)
	
	for KeyToFind in DictOfDir:
		print("Key is {Key}, dir is {Dir}.".format(Key=KeyToFind, Dir=DictOfDir[KeyToFind]))
#		for MediaFile in ListOfMediaFile:
#			print("Keyword is {KeyWord}, Mediafile is {KeyMediaFile}.".format(KeyWord=Dir, KeyMediaFile=MediaFile))

except Exception as err:
	print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))

