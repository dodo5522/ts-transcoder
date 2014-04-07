#!/usr/bin/env python2.7

"""
	module:		photosort

	This script to make directory of date which the photo is taken, and move the photo into the directory.

	argument1:	root directory path of source
	argument2:	root directory path of destination
"""

import os,glob,sys,string,re
import shutil
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file, __version__

class PhotoSort:
	def __init__(self, stringPathOfRoot, listExtentions):
		extentions = []
		extention_lower = []
		extention_upper = []
		
		for extention in listExtentions:
			extention_lower.append(extention.lower())
			extention_upper.append(extention.upper())
		
		extentions.extend(extention_lower)
		extentions.extend(extention_upper)
		
		setattr(self, "_listExtentions", extentions)
		setattr(self, "_stringPathOfRoot", stringPathOfRoot)
	
	def getTargetDirectory(self):
		return self._stringPathOfRoot
	
	def getFileExtentionsList(self):
		return self._listExtentions
	
	def sortFiles(self):
		for fileFound in os.listdir(self._stringPathOfRoot):
			pathSrcImg = os.path.join(self._stringPathOfRoot, fileFound)
			if not os.path.isfile(pathSrcImg):
				continue
			
			try:
				objImgFile = None
				(pathSrcImgWoExt, ext) = os.path.splitext(fileFound)
				
				# if error, exception process continue to the next loop.
				index = self._listExtentions.index(ext[1:])
				
				objImgFile = open(pathSrcImg, "rb")
				exif_data = process_file(objImgFile, stop_tag='EXIF DateTimeOriginal')
				objImgFile.close()
				
				# thumbnail binary data is not used in this script.
				unusedParam = 'JPEGThumbnail'
				if unusedParam in exif_data:
					del exif_data[unusedParam]
				
				# EXIF DateTimeOriginal is stored with this format "YYYY:MM:DD HH:MM:SS".
				dateAndTime = exif_data['EXIF DateTimeOriginal']
				
				if hasattr(dateAndTime, 'printable'):
					# FIXME: want to translate directory name with some optional character.
					(date, time) = dateAndTime.printable.split(' ')
					pathDstDir = os.path.join(os.path.dirname(pathSrcImg), date.translate(None, ':'))
					pathDstImg = os.path.join(pathDstDir, os.path.basename(pathSrcImg))
					
					# create directory to move.
					if not os.path.isdir(pathDstDir):
						os.mkdir(pathDstDir)
					shutil.move(pathSrcImg, pathDstImg)
				
			except Exception as err:
				print str(type(err)) + " occurs with message \"" + err.message + "\"."
				continue
			
			finally:
				if objImgFile is not None:
					objImgFile.close()
	
	def showHelp(self):
		print "this_script path_to_root_directory"
	
	def __del__(self):
		print "destructor is called."

# main routine for executed as python script
if __name__ == '__main__':
	try:
		pathRoot = "/Users/takashi/Pictures"
		extList = ["jpg","png"]
		
		objPhotoSort = PhotoSort(pathRoot,extList)
		print objPhotoSort.getFileExtentionsList()
		
		objPhotoSort.sortFiles()
		

	except Exception as err:
		print "Exception type is ",type(err)
		print "Exception arg is ",err.args
		print "Exception is ",err
