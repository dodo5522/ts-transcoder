#!/usr/bin/env python3.2

import os,sys,string,re
import shutil as sh
debug = False

'''
DESCRIPTION
	To find all target directories to move media files.
	The target directories' name is the keyword to find media files.
'''
def get_dict_dirs(path_root=""):
	dict_dirs = {}
	for dir_found in os.listdir(path_root):
		if os.path.isdir(os.path.join(path_root, dir_found)):
			dict_dirs[dir_found] = os.path.join(path_root, dir_found)
	
	if debug == True:
		print("Found directory:")
		for key_found in dict_dirs:
			print(" {key_found}".format(key_found=key_found))
	
	return dict_dirs

'''
DESCRIPTION
	To find all media files to be moved.
'''
def get_dict_mediafiles(path_root="", keyword=""):
	dict_mediafiles = {}
	for file_found in os.listdir(path_root):
		if os.path.isfile(os.path.join(path_root, file_found)):
			ReObj = re.search('.*' + keyword + '.*\.mp4', file_found)
			if ReObj != None:
				dict_mediafiles[file_found] = os.path.join(path_root, file_found)
	
	if debug == True:
		print("Found media file:")
		for key in dict_mediafiles:
			print(" {mediafile_found}".format(mediafile_found=key))
	
	return dict_mediafiles

if __name__ == '__main__':
	try:
		argvs = sys.argv
		argc = len(argvs)
		
		if argc != 3:
			print("Error! Argument is not enough.")
			sys.exit()
		
		path_mediafiles_located = argvs[1]
		path_root_moving = argvs[2]
		dict_dirs_moving = get_dict_dirs(path_root_moving)
		
		for dir_found in dict_dirs_moving:
			print("Keyword : {keyword}".format(keyword=dir_found))
			dict_mediafiles = get_dict_mediafiles(path_mediafiles_located, dir_found)
			
			for file_media in dict_mediafiles:
				path_media_src = dict_mediafiles[file_media]
				path_media_dst = os.path.join(dict_dirs_moving[dir_found],file_media)
				
				if os.path.isfile(path_media_dst):
					print("{mediafile} for destination already exists, so source file is removed.".format(mediafile=path_media_dst))
					os.remove(path_media_src)
				else:
					print("Found media file : {mediafile}".format(mediafile=path_media_src)) 
					print("Target to move : {dir_moving}".format(dir_moving=dict_dirs_moving[dir_found]))
					sh.move(path_media_src, path_media_dst)
	
	except Exception as err:
		print("Error type is {ErrType}, {Args}.".format(ErrType=type(err),Args=err.args))

