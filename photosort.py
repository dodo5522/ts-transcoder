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
	def __init__(self, aTargetDirectory, aExtList):
		self.targetDirectory = aTargetDirectory
		self.fileExtentions = aExtList
	
	def getTargetDirectory(self):
		return self.targetDirectory
	
	def getFileExtentionsList(self):
		return self.fileExtentions
	
	def getPhotoFilesPathList(self):
		foundFilesPathList = []
		for fileExtention in self.fileExtentions:
			fileNameWithWildCard = "*."+fileExtention
			pathWithFileNamePattern = os.path.join(self.targetDirectory,fileNameWithWildCard)
			foundFilesPathList.append(glob.glob(pathWithFileNamePattern))
		
		return foundFilesPathList
	
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
		pathsOfPhoto = objPhotoSort.getPhotoFilesPathList()
		print "Photo files paths are",pathsOfPhoto

	except Exception as err:
		print "Exception type is ",type(err)
		print "Exception arg is ",err.args
		print "Exception is ",err
	
	else:
		print "else"
	
	finally:
		print "finally"

