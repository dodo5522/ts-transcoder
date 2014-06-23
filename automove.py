#!/usr/bin/env python2.7

import os,sys,re,glob,shutil
import platform,unicodedata
import logging,traceback

'''
DESCRIPTION
	To find all target directories to move media files.
	The target directories' name is the keyword to find media files.
'''
class AutoMove(object):
	def get_dict_dirs(self, path_root):
		dict_dirs = {}
		for dir_found in os.listdir(path_root):
			if os.path.isdir(os.path.join(path_root, dir_found)):
				dict_dirs[dir_found] = os.path.join(path_root, dir_found)
		
		logging.debug("Found directory:{FOUND_KEYS}".format(FOUND_KEYS=dict_dirs.keys()))
		return dict_dirs
	
	def get_dict_mediafiles(self, path_root, keyword):
		dict_mediafiles = {}
		for file_found in glob.glob(os.path.join(path_root, '*.mp4')):
			if os.path.isfile(file_found):
				objre = re.search(keyword, file_found)
				if objre != None:
					file_name = os.path.basename(file_found)
					dict_mediafiles[file_name] = os.path.join(file_found)
		
		logging.debug("Found media:{FOUND_MEDIA}".format(FOUND_MEDIA=dict_mediafiles.keys()))
		return dict_mediafiles

if __name__ == '__main__':
	try:
		argvs = sys.argv
		argc = len(argvs)
		
		if argc != 3:
			logging.error("Argument is not enough.")
			sys.exit()
		
		path_mediafiles_located = argvs[1]
		path_root_moving = argvs[2]
		
		logging.basicConfig(level=logging.DEBUG)
		obj = AutoMove()
		dict_dirs_moving = obj.get_dict_dirs(path_root_moving)
		
		for dir_found in dict_dirs_moving:
			logging.debug("Target dir:{DIR_TARGET}".format(DIR_TARGET=dir_found))
			dict_mediafiles = obj.get_dict_mediafiles(path_mediafiles_located, dir_found)
			
			for file_media in dict_mediafiles:
				logging.debug("Found media:{FILE_MEDIA}".format(FILE_MEDIA=file_media)) 
				path_media_src = dict_mediafiles[file_media]
				path_media_dst = os.path.join(dict_dirs_moving[dir_found],file_media)
				
				if os.path.isfile(path_media_dst):
					logging.warn("{FILE_MEDIA} already exists so remove it.".format(FILE_MEDIA=path_media_dst))
					os.remove(path_media_src)
				else:
					tmp_file_media = file_media
					tmp_dir_found = dir_found
					if platform.system() == 'Darwin':
						file_media_unicode = tmp_file_media.decode('utf-8')
						dir_found_unicode = tmp_dir_found.decode('utf-8')
						tmp_file_media = unicodedata.normalize('NFC', file_media_unicode).encode('utf-8')
						tmp_dir_found = unicodedata.normalize('NFC', dir_found_unicode).encode('utf-8')
					logging.info("Move {FILE_MEDIA} to {DIR_TARGET}".format(FILE_MEDIA=tmp_file_media, DIR_TARGET=tmp_dir_found))
					shutil.move(path_media_src, path_media_dst)
	
	except Exception as err:
		traceback.print_exc()

