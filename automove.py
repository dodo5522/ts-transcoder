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
    def __init__(self, path_dest_root, path_src_file):
        setattr(self, '_list_dest_paths', None)
        self._get_dest_dirs(path_dest_root)

    def _get_dest_dirs(self, path_dest_root):
        self._list_dest_paths = []
        for dir_found in os.listdir(path_dest_root):
            if os.path.isdir(os.path.join(path_dest_root, dir_found)):
                self._list_dest_paths.append(os.path.join(path_dest_root, dir_found))

        logging.debug("Found directory:{FOUND_KEYS}".format(FOUND_KEYS=self._list_dest_paths))
        return self._list_dest_paths

class AutoSearchMove(AutoMove):
    def __init__(self, path_dest_root, path_src_root):
        AutoMove.__init__(self, path_dest_root, None)
        setattr(self, '_dict_mediafiles', None)
        self._get_dict_mediafiles(path_src_root)

    def _get_dict_mediafiles(self, path_src_root):
        self._dict_mediafiles = {}
        for path_dest in self._list_dest_paths:
            list_mediafiles = []
            keyword = os.path.basename(path_dest)
            for file_found in glob.glob(os.path.join(path_src_root, '*' + keyword + '*.mp4')):
                if not os.path.isfile(file_found):
                    continue
                list_mediafiles.append(file_found)
            self._dict_mediafiles[keyword] = list_mediafiles

        logging.debug("Found media:{FOUND_MEDIA}".format(FOUND_MEDIA=self._dict_mediafiles.items()))
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
        parser = argparse.ArgumentParser(description='This script to move media files into the directory path named with keyword.')
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

