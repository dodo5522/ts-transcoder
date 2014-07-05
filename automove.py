#!/usr/bin/env python2.7

import os, glob, shutil
import argparse
import logging, traceback
from conv_uni import *

'''
DESCRIPTION
    To find all target directories to move media files.
    The target directories' name is the keyword to find media files.
'''
class AutoMove(object):
    def __init__(self, path_dest_root):
        self._path_dest_root = path_dest_root
        self._dict_paths_dest = {}
        for dir_found in os.listdir(self._path_dest_root):
            path_found = os.path.join(self._path_dest_root, dir_found)
            if os.path.isdir(path_found):
                self._dict_paths_dest[dir_found] = path_found
        logging.debug(u"Found dirs:{DIRS}".format(DIRS=','.join(self._dict_paths_dest.keys())))

    def move(self, path_src_file):
        for dir_target in self._dict_paths_dest:
            if dir_target in path_src_file:
                path_dst = self._dict_paths_dest[dir_target]
                shutil.move(path_src_file, path_dst)
                logging.info(u"Move {MEDIA} to {TARGET}".format(MEDIA=path_src_file, TARGET=path_dst))
                return True
        return False

class AutoSearchMove(AutoMove):
    def __init__(self, path_dest_root, path_src_root):
        AutoMove.__init__(self, path_dest_root)
        self._dict_mediafiles = {}
        for keyword in self._dict_paths_dest:
            list_mediafiles = []
            for file_found in glob.glob(os.path.join(path_src_root, u'*' + keyword + u'*.mp4')):
                if not os.path.isfile(file_found):
                    continue
                list_mediafiles.append(file_found)
            self._dict_mediafiles[keyword] = list_mediafiles
        logging.debug(u"Found media:{MEDIA}".format(MEDIA=','.join(self._dict_mediafiles.keys())))

    def move(self):
        for keyword in self._dict_paths_dest:
            logging.debug(u"Target dir:{PATH_TARGET}".format(PATH_TARGET=self._dict_paths_dest[keyword]))

            for path_media_src in self._dict_mediafiles[keyword]:
                logging.debug(u"Found media:{PATH_MEDIA}".format(PATH_MEDIA=path_media_src)) 
                path_media_dst = os.path.join(self._dict_paths_dest[keyword], os.path.basename(path_media_src))

                if os.path.isfile(path_media_dst):
                    logging.warn(u"{PATH_MEDIA} already exists so remove it.".format(PATH_MEDIA=path_media_dst))
                    os.remove(path_media_src)
                else:
                    tmp_path_media = path_media_src
                    tmp_path_target = self._dict_paths_dest[keyword]
                    logging.info(u"Move {PATH_MEDIA} to {PATH_TARGET}".format(PATH_MEDIA=tmp_path_media, PATH_TARGET=tmp_path_target))

                    shutil.move(path_media_src, path_media_dst)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='This script to move media files into the directory path named with keyword.')
        parser.add_argument('-f', '--path-source-file', \
                action='store', \
                default=None, \
                required=False, \
                help='Path of media file which is going to be moved.')
        parser.add_argument('-s', '--path-source-dir', \
                action='store', \
                default=None, \
                required=False, \
                help='Path of root directory having media files.')
        parser.add_argument('-d', '--path-destination-dir', \
                action='store', \
                default=None, \
                required=True, \
                help='Path of destination directory path which has child directories named with keyword.')
        parser.add_argument('--stub', \
                action='store', \
                default=False, \
                required=False, \
                help='Use stub to debug if this flag is set.')
        parser.add_argument('--log-level', \
                action='store', \
                default='info', \
                required=False, \
                help='Set log level.')
        args = parser.parse_args()

        numeric_level = getattr(logging, args.log_level.upper(), None)
        if isinstance(numeric_level, int):
            logging.basicConfig(level=numeric_level)
        else:
            logging.basicConfig(level=logging.INFO)

        if args.path_source_file is not None:
            obj_automv = AutoMove(str_to_uni(args.path_destination_dir))
            obj_automv.move(str_to_uni(args.path_source_file))

        if args.path_source_dir is not None:
            obj_searchmv = AutoSearchMove(\
                    str_to_uni(args.path_destination_dir), \
                    str_to_uni(args.path_source_dir))
            obj_searchmv.move()

    except Exception as err:
        traceback.print_exc()

