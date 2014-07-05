#!/usr/bin/env python2.7

import os, glob, shutil
import argparse
import platform, unicodedata
import logging, traceback

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
        logging.debug("Found dirs:{DIRS}".format(DIRS=','.join(self._dict_paths_dest.keys())))

    def move(self, path_src_file):
        for dir_target in self._dict_paths_dest:
            if dir_target in path_src_file:
                shutil.move(path_src_file, self._dict_paths_dest[dir_target])
                return True
        return False

class AutoSearchMove(AutoMove):
    def __init__(self, path_dest_root, path_src_root):
        AutoMove.__init__(self, path_dest_root)
        self._dict_mediafiles = {}
        for keyword in self._dict_paths_dest:
            list_mediafiles = []
            for file_found in glob.glob(os.path.join(path_src_root, '*' + keyword + '*.mp4')):
                if not os.path.isfile(file_found):
                    continue
                list_mediafiles.append(file_found)
            self._dict_mediafiles[keyword] = list_mediafiles
        logging.debug("Found media:{MEDIA}".format(MEDIA=','.join(self._dict_mediafiles.keys())))

    def move_mediafiles(self):
        for keyword in self._dict_paths_dest:
            logging.debug("Target dir:{PATH_TARGET}".format(PATH_TARGET=self._dict_paths_dest[keyword]))

            for path_media_src in self._dict_mediafiles[keyword]:
                logging.debug("Found media:{PATH_MEDIA}".format(PATH_MEDIA=path_media_src)) 
                path_media_dst = os.path.join(self._dict_paths_dest[keyword], os.path.basename(path_media_src))

                if os.path.isfile(path_media_dst):
                    logging.warn("{PATH_MEDIA} already exists so remove it.".format(PATH_MEDIA=path_media_dst))
                    os.remove(path_media_src)
                else:
                    tmp_path_media = path_media_src
                    tmp_path_target = self._dict_paths_dest[keyword]
                    if platform.system() == 'Darwin':
                        file_media_unicode = tmp_path_media.decode('utf-8')
                        dir_found_unicode = tmp_path_target.decode('utf-8')
                        tmp_path_media = unicodedata.normalize('NFC', file_media_unicode).encode('utf-8')
                        tmp_path_target = unicodedata.normalize('NFC', dir_found_unicode).encode('utf-8')
                    logging.info("Move {PATH_MEDIA} to {PATH_TARGET}".format(PATH_MEDIA=tmp_path_media, PATH_TARGET=tmp_path_target))

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
                required=True, \
                help='Path of media files which are going to be moved.')
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

        obj = AutoSearchMove(args.path_destination_dir, args.path_source_dir)
        obj.move_mediafiles()

    except Exception as err:
        traceback.print_exc()

