#!/usr/bin/python

"""
	module:		photosort

	This script to make directory of date which the photo is taken, and move the photo into the directory.

	argument1:	root directory path of source
	argument2:	root directory path of destination
"""

import os,glob,sys,string,re
#import pyexiv2 as exiv

class PhotoSort:
	_stringPathOfRoot = ''
	_listExtentions = [] 
	
	def __init__(self, stringPathOfRoot, listExtentions):
		self._stringPathOfRoot = stringPathOfRoot
		self._listExtentions = listExtentions
	
	def getTargetDirectory(self):
		return self._stringPathOfRoot
	
	def getFileExtentionsList(self):
		return self._listExtentions
	
	def getPhotoFilesPathList(self, isExtentionsLowerOnly):
		listExtentionsToFind = []
		listPathOfFiles = []
		
		for stringExtention in self._listExtentions:
			listExtentionsToFind.append(stringExtention.lower())
			if not isExtentionsLowerOnly:
				listExtentionsToFind.append(stringExtention.upper())
		
		for stringExtention in listExtentionsToFind:
			stringPathToFind = os.path.join(self._stringPathOfRoot,"*."+stringExtention)
			listPathOfFiles.append(glob.glob(stringPathToFind))
		
		return listPathOfFiles
	
	def makeDirAndSortPhotoFiles(self):
		return True
	
	def showHelp(self):
		print "this_script path_to_root_directory"
	
	def __del__(self):
		print "destructor is called."

# main routine for executed as python script
if __name__ == '__main__':
	try:
		if len(sys.argv) != 2:
			raise ValueError("invalid arguments")
		elif sys.argv[1] == "error":
			raise Exception("exception test")
		
		pathRoot = sys.argv[1]
		extList = ["jpg","png"]
		
		objPhotoSort = PhotoSort(pathRoot,extList)
		print "Photo files paths are",objPhotoSort.getPhotoFilesPathList(False)

	except Exception as err:
		print "Exception type is ",type(err)
		print "Exception arg is ",err.args
		print "Exception is ",err
	
	else:
		print "else"
	
	finally:
		print "finally"

