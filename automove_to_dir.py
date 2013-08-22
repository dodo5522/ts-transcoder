#!/usr/bin/python3

import os,sys,string,re
import shutil as sh
DEBUG_PYTHON = False

###################
# sub routine
###################

'''
DESCRIPTION
	To find all target directories to move media files.
	The target directories' name is the keyword to find media files.
'''
def GetListOfDirectoryToMove(RootDirectory=""):
	DictOfDirectoryToMove = {}
	for FileOrDir in os.listdir(RootDirectory):
		if os.path.isdir(os.path.join(RootDirectory, FileOrDir)):
			DictOfDirectoryToMove[FileOrDir] = os.path.join(RootDirectory, FileOrDir)
	
	if DEBUG_PYTHON == True:
		print("Found directory:")
		for FoundKey in DictOfDirectoryToMove:
			print(" {FoundKey}".format(FoundKey=FoundKey))
	
	return DictOfDirectoryToMove

'''
DESCRIPTION
	To find all media files to be moved.
'''
def FindMediaFileWithKeyword(RootDirectory="", KeyWord=""):
	DictOfMediaFile = {}
	for FileOrDir in os.listdir(RootDirectory):
		if os.path.isfile(os.path.join(RootDirectory, FileOrDir)):
			MediaFile = FileOrDir
			ReObj = re.search('.*' + KeyWord + '.*\.mp4', MediaFile)
			if ReObj != None:
				DictOfMediaFile[MediaFile] = os.path.join(RootDirectory, MediaFile)
	
	if DEBUG_PYTHON == True:
		print("Found media file:")
		for FoundMediaFile in DictOfMediaFile:
			print(" {FoundMediaFile}".format(FoundMediaFile=FoundMediaFile))
	
	return DictOfMediaFile

###################
# main routine
###################

try:
	ARGVS = sys.argv
	ARGC = len(ARGVS)
	OWN = ARGVS[0]
	
	if ARGC != 3:
		print("Error! Argument is not enough.")
		print("{Own} dir_of_src dir_of_dst(includes key directories)".format(Own=OWN))
		sys.exit()
	
	DIR_MEDIA = ARGVS[1]
	DIR_TARGET = ARGVS[2]
	
	DictOfDir = GetListOfDirectoryToMove(DIR_TARGET)
	for KeyToFind in DictOfDir:
		DictOfMediaFile = FindMediaFileWithKeyword(DIR_MEDIA, KeyToFind)
		for FoundMediaFile in DictOfMediaFile:
			print("Keyword : {Key}".format(Key=KeyToFind))
			if os.path.isdir(DictOfDir[KeyToFind]):
				print("{Dir} already exists so removed.".format(Dir=DictOfDir[KeyToFind]))
				os.remove(DictOfMediaFile[FoundMediaFile])
			else:
				print("Found media file : {File}".format(File=DictOfMediaFile[FoundMediaFile]))
				print("Target to move : {Dir}".format(Dir=DictOfDir[KeyToFind]))
				sh.move(DictOfMediaFile[FoundMediaFile], DictOfDir[KeyToFind])

except Exception as err:
	print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))

