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

def FindMediaFileWithKeyword(RootDirectory="", KeyWord=""):
	print("Found media file:")
	
	DictOfMediaFile = {}
	for FileOrDir in os.listdir(RootDirectory):
		if os.path.isfile(os.path.join(RootDirectory, FileOrDir)):
			MediaFile = FileOrDir
			ReObj = re.search('.*' + KeyWord + '.*', MediaFile)
			if ReObj != None:
				print(" {File}".format(File=MediaFile))
				DictOfMediaFile[MediaFile] = os.path.join(RootDirectory, MediaFile)
	
	return DictOfMediaFile

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
		DictOfMediaFile = FindMediaFileWithKeyword(DIR_MEDIA, KeyToFind)
		for FoundMediaFile in DictOfMediaFile:
			print("Keyword          : {Key}".format(Key=KeyToFind))
			print("Found media file : {File}".format(File=DictOfMediaFile[FoundMediaFile]))
			print("Target to move   : {Dir}".format(Dir=DictOfDir[KeyToFind]))

except Exception as err:
	print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))

