#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,glob,sys,string,re
import shutil
import argparse
from exifread import process_file, __version__

TAG_DATE_TIME = 'EXIF DateTimeOriginal'

class PhotoSort:
	def __init__(self, path_root_src=None, path_root_dst=None, listExtentions=None, debug=False):
		extentions = []
		extention_lower = []
		extention_upper = []
		
		for extention in listExtentions:
			extention_lower.append(extention.lower())
			extention_upper.append(extention.upper())
		
		extentions.extend(extention_lower)
		extentions.extend(extention_upper)
		
		setattr(self, "_listExtentions", extentions)
		setattr(self, "_path_root_src", path_root_src)
		setattr(self, "_path_root_dst", path_root_dst)
		setattr(self, "_debug", debug)
	
	def getTargetDirectory(self):
		return self._path_root_src
	
	def getFileExtentionsList(self):
		return self._listExtentions
	
	def sortFiles(self):
		for fileFound in os.listdir(self._path_root_src):
			pathSrcImg = os.path.join(self._path_root_src, fileFound)
			if not os.path.isfile(pathSrcImg):
				continue
			
			try:
				objImgFile = None
				(pathSrcImgWoExt, ext) = os.path.splitext(fileFound)
				
				# if error, exception process continue to the next loop.
				index = self._listExtentions.index(ext[1:])
				
				objImgFile = open(pathSrcImg, "rb")
				exif_data = process_file(objImgFile, stop_tag=TAG_DATE_TIME)
				objImgFile.close()
				
				# thumbnail binary data is not used in this script.
				unusedParam = 'JPEGThumbnail'
				if unusedParam in exif_data:
					del exif_data[unusedParam]
				
				# EXIF DateTimeOriginal is stored with this format "YYYY:MM:DD HH:MM:SS".
				dateAndTime = exif_data[TAG_DATE_TIME]
				
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
				if self._debug == True:
					print str(type(err)) + " occurs with message \"" + err.message + "\"."
				continue
			
			finally:
				if objImgFile is not None:
					objImgFile.close()
	
	def __del__(self):
		print "destructor is called."

# main routine for executed as python script
if __name__ == '__main__':
	try:
		parser = argparse.ArgumentParser(description='This script to make directory of date which the photo is taken, and move the photo into the directory.')
		parser.add_argument('path_root_src', \
				action='store', \
				nargs=None, \
				const=None, \
				default=None, \
				type=str, \
				choices=None, \
				help='Directory path where your taken photo files are located.', \
				metavar=None)
		parser.add_argument('-d', '--path-root-dst', \
				action='store', \
				nargs='?', \
				const=None, \
				default=None, \
				type=str, \
				choices=None, \
				help='Directory path where you want to create date folder and locate photo files. (default: same as source directory)', \
				metavar=None)
		parser.add_argument('-e', '--sort-files-extentions', \
				action='store', \
				nargs='+', \
				const=None, \
				default=['jpg'], \
				type=str, \
				choices=None, \
				help='Extentions of file which you want to sort. (default: jpg)', \
				metavar=None)
		parser.add_argument('--debug', \
				action='store_true', \
				default=False, \
				help='debug mode if this flag is set (default: False)')
		args = parser.parse_args()
		
		objPhotoSort = PhotoSort(args.path_root_src, args.path_root_dst, args.sort_files_extentions, args.debug)
		objPhotoSort.sortFiles()
		
	except Exception as err:
		if args.debug == True:
			print "Exception type is ",type(err)
			print "Exception arg is ",err.args
			print "Exception is ",err
