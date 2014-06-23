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
	def __init__(self, path_src_root, path_dest_root):
		list_dest_paths = []
		for dir_found in os.listdir(path_dest_root):
			if os.path.isdir(os.path.join(path_dest_root, dir_found)):
				list_dest_paths.append(os.path.join(path_dest_root, dir_found))
		
		logging.debug("Found directory:{FOUND_KEYS}".format(FOUND_KEYS=list_dest_paths))
		setattr(self, "_list_dest_paths", list_dest_paths)
		
		dict_mediafiles = {}
		for path_dest in self._list_dest_paths:
			list_mediafiles = []
			keyword = os.path.basename(path_dest)
			for file_found in glob.glob(os.path.join(path_src_root, '*' + keyword + '*.mp4')):
				if not os.path.isfile(file_found):
					continue
				list_mediafiles.append(file_found)
			dict_mediafiles[keyword] = list_mediafiles
		
		logging.debug("Found media:{FOUND_MEDIA}".format(FOUND_MEDIA=dict_mediafiles.items()))
		setattr(self, "_dict_mediafiles", dict_mediafiles)
	
	def get_dest_dirs(self):
		return self._list_dest_paths
	
	def get_dict_mediafiles(self):
		return self._dict_mediafiles
	
	def move_mediafiles(self):
		for path_dest in self._list_dest_paths:
			keyword = os.path.basename(path_dest)
			logging.debug("Target dir:{PATH_TARGET}".format(PATH_TARGET=path_dest))
			
			for path_media_src in self._dict_mediafiles[keyword]:
				logging.debug("Found media:{PATH_MEDIA}".format(PATH_MEDIA=path_media_src)) 
				path_media_dst = os.path.join(path_dest, os.path.basename(path_media_src))
				
				if os.path.isfile(path_media_dst):
					logging.warn("{PATH_MEDIA} already exists so remove it.".format(PATH_MEDIA=path_media_dst))
					os.remove(path_media_src)
				else:
					tmp_path_media = path_media_src
					tmp_path_target = path_dest
					if platform.system() == 'Darwin':
						file_media_unicode = tmp_path_media.decode('utf-8')
						dir_found_unicode = tmp_path_target.decode('utf-8')
						tmp_path_media = unicodedata.normalize('NFC', file_media_unicode).encode('utf-8')
						tmp_path_target = unicodedata.normalize('NFC', dir_found_unicode).encode('utf-8')
					logging.info("Move {PATH_MEDIA} to {PATH_TARGET}".format(PATH_MEDIA=tmp_path_media, PATH_TARGET=tmp_path_target))
					
					shutil.move(path_media_src, path_media_dst)

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
		
		obj = AutoMove(path_mediafiles_located, path_root_moving)
		obj.move_mediafiles()
		
	except Exception as err:
		traceback.print_exc()

