#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from importlib import import_module
import os
import glob
import sys
import time
import shutil
import argparse
import logging
import mediainfo
import traceback
from exifread import process_file


TAG_DATE_TIME = 'EXIF DateTimeOriginal'


def init_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='This script to make directory of date which the photo is taken, and move the photo into the directory.')
    parser.add_argument(
        'path_root_src',
        action='store',
        nargs=None,
        const=None,
        default=None,
        type=str,
        choices=None,
        help='Directory path where your taken photo files are located.',
        metavar=None)
    parser.add_argument(
        '-d', '--path-root-dst',
        action='store',
        nargs='?',
        const=None,
        default='',
        type=str,
        choices=None,
        help='Directory path where you want to create date folder and locate photo files. (default: same as source directory)',
        metavar=None)
    parser.add_argument(
        '-p', '--sort-photo-extentions',
        action='store',
        nargs='+',
        const=None,
        default=(),
        type=str,
        choices=None,
        help='Extentions of photo file which you want to sort. (default: jpg)',
        metavar=None)
    parser.add_argument(
        '-v', '--sort-video-extentions',
        action='store',
        nargs='+',
        const=None,
        default=(),
        type=str,
        choices=None,
        help='Extentions of video file which you want to sort. (default: jpg)',
        metavar=None)
    parser.add_argument(
        '-l', '--delimiter',
        action='store',
        default='',
        type=str,
        choices=None,
        required=False,
        help='A character as delimiter which you want to set the name of date folder like "2014-05-01". (default: none)',
        metavar=None)
    parser.add_argument(
        '--subdir-year',
        action='store_true',
        default=False,
        required=False,
        help='Generate sub directory of year if this is set.')
    parser.add_argument(
        '--subdir-month',
        action='store_true',
        default=False,
        required=False,
        help='Generate sub directory of month if this is set.')
    parser.add_argument(
        '--copy',
        action='store_true',
        default=False,
        required=False,
        help='Copy media files but not move.')
    parser.add_argument(
        '--callback-function',
        action='store',
        default=None,
        type=str,
        choices=None,
        required=False,
        help='Function to be callback when copying/moving a photo finished. The format is like "/User/takashi/flickr_uploader/flickr_uploader:upload?key=xxx&param=yyy". The "upload" function should have an argument "path_to_photo_uploading" as first and another args is passed to keyword arguments. (default: none)',
        metavar=None)
    parser.add_argument(
        '--debug',
        action='store',
        default='info',
        required=False,
        help='debug mode if this flag is set (default: info)')

    return parser.parse_args(args)


class SortFiles(object):
    def __init__(self, ext_src=['jpg', ], path_root_src='.', path_root_dst='.', delimiter='', **kwargs):
        self._ext_src = []
        for extention in ext_src:
            self._ext_src.append(extention.lower())
            self._ext_src.append(extention.upper())

        self._path_root_src = path_root_src
        self._path_root_dst = path_root_dst
        self._delimiter = delimiter
        self._subdir = kwargs['subdir']
        self._is_copy = kwargs['is_copy']

        logging.debug("_ext_src : " + ','.join(self._ext_src))
        logging.debug("_path_root_src : " + self._path_root_src)
        logging.debug("_path_root_dst : " + self._path_root_dst)
        logging.debug("_delimiter : " + self._delimiter)
        logging.debug("_subdir : " + ','.join([str(subdir) for subdir in self._subdir]))

        callback_full = kwargs.get('callback_function')
        self._callback_module_path = os.path.dirname(callback_full) if callback_full else ""
        self._callback_module = os.path.basename(callback_full).split(":")[0] if callback_full else ""
        self._callback_function = os.path.basename(callback_full).split(":")[1].split("?")[0] if callback_full else ""

        self._callback_kwargs = {}
        if callback_full and len(os.path.basename(callback_full).split(":")[1].split("?")) >= 2:
            kw_strs = os.path.basename(callback_full).split(":")[1].split("?")[1].split("&")
            self._callback_kwargs = {kw_str.split("=")[0]: kw_str.split("=")[1] for kw_str in kw_strs}

        logging.debug("callback_module_path : {}".format(self._callback_module_path))
        logging.debug("callback_module : {}".format(self._callback_module))
        logging.debug("callback_function : {}".format(self._callback_function))

    def get_date_of_file(self, path_file_src):
        epoc_time = os.stat(path_file_src)
        mtime = time.gmtime(epoc_time.st_mtime)
        date = '{year:04d}-{month:02d}-{day:02d}'.format(year=mtime.tm_year, month=mtime.tm_mon, day=mtime.tm_mday)
        logging.debug('{file_src} has {mtime}.'.format(file_src=path_file_src, mtime=mtime))
        return date

    def sort_files(self):
        for extention in self._ext_src:
            pattern_search = '*.{0}'.format(extention)
            paths_src_img = glob.glob(os.path.join(self._path_root_src, pattern_search))

            for path_src_img in paths_src_img:
                if not os.path.isfile(path_src_img):
                    continue

                try:
                    # get date directory name from specified file.
                    date = self.get_date_of_file(path_src_img)
                    (year, month, day) = date.split('-')
                    date = date.replace('-', self._delimiter)

                    logging.debug("date is {0}.".format(date))
                except Exception as e:
                    logging.info("{}: {} ".format(path_src_img, e))
                    continue

                # if destination path is not set, destination is same as source.
                if len(self._path_root_dst) is not 0:
                    path_dst_dir = self._path_root_dst
                else:
                    path_dst_dir = os.path.dirname(path_src_img)

                # if the first subdir is False, sub directory is not created.
                path_sub_dir = ''
                if self._subdir[0]:
                    path_sub_dir = year
                    if self._subdir[1]:
                        path_sub_dir = os.path.join(path_sub_dir, month)

                if len(path_sub_dir) is not 0:
                    path_dst_dir = os.path.join(path_dst_dir, path_sub_dir)

                # nearly same directory exists, use it.
                path_dst_dir = os.path.join(path_dst_dir, date)
                path_dst_dirs = glob.glob("{0}*".format(path_dst_dir))
                path_dst_dir = path_dst_dirs[0] if len(path_dst_dirs) else path_dst_dir

                path_dst_img = os.path.join(path_dst_dir, os.path.basename(path_src_img))

                # create directory to move.
                if not os.path.isdir(path_dst_dir):
                    os.makedirs(path_dst_dir)

                logging.debug("path_src_img is {0}.".format(path_src_img))
                logging.debug("path_dst_img is {0}.".format(path_dst_img))

                logging.info("{0}{1} {2} to {3}.".format(
                    "skip " if os.path.isfile(path_dst_img) else "",
                    "copying" if self._is_copy else "moving",
                    path_src_img, path_dst_img))

                if not os.path.isfile(path_dst_img):
                    if self._is_copy:
                        shutil.copy2(path_src_img, path_dst_img)
                    else:
                        shutil.move(path_src_img, path_dst_img)

                    if self._callback_function and (
                            os.path.splitext(path_dst_img)[1].lower() == '.mp4' or
                            os.path.splitext(path_dst_img)[1].lower() == '.avi' or
                            os.path.splitext(path_dst_img)[1].lower() == '.mov' or
                            os.path.splitext(path_dst_img)[1].lower() == '.jpg' or
                            os.path.splitext(path_dst_img)[1].lower() == '.png'):
                        logging.info("calling {}:{} on {}.".format(
                            self._callback_module, self._callback_function, self._callback_module_path))

                        sys.path.append(self._callback_module_path)
                        mod_ = import_module(self._callback_module)
                        callback_ = getattr(mod_, self._callback_function)

                        callback_(path_dst_img, **self._callback_kwargs)

    def __del__(self):
        pass


class SortPhotoFiles(SortFiles):
    def get_date_of_file(self, path_src_img):
        obj_img = open(path_src_img, "rb")
        exif_data = process_file(obj_img, stop_tag=TAG_DATE_TIME)
        obj_img.close()

        # thumbnail binary data is not used in this script.
        tag_unused = 'JPEGThumbnail'
        if tag_unused in exif_data:
            del exif_data[tag_unused]

        # EXIF DateTimeOriginal is stored with this format "YYYY:MM:DD HH:MM:SS".
        date_and_time = exif_data[TAG_DATE_TIME]

        # return date with '-' like '2014-05-01'
        (date, time) = date_and_time.printable.split(' ')
        date = date.replace(':', '-')
        return date


class SortVideoFiles(SortFiles):
    def get_date_of_file(self, path_src_mov):
        obj_media = mediainfo.MediaInfo(path_src_mov, None)
        media_data = obj_media.info_video.get_encoded_date()

        if media_data is not None:
            # return date with '-' like '2014-05-01'
            date_and_time = media_data.split()
            date = date_and_time[1]
        else:
            date = SortFiles.get_date_of_file(self, path_src_mov)
        return date


if __name__ == '__main__':
    try:
        args = init_args()

        if hasattr(logging, args.debug.upper()):
            numeric_level = getattr(logging, args.debug.upper())
            if isinstance(numeric_level, int):
                logging.basicConfig(level=numeric_level)

        obj_sort = []

        if len(args.sort_photo_extentions):
            obj_sort.append(SortPhotoFiles(
                path_root_src=args.path_root_src,
                path_root_dst=args.path_root_dst,
                ext_src=args.sort_photo_extentions,
                delimiter=args.delimiter,
                subdir=(
                    args.subdir_year,
                    args.subdir_month),
                is_copy=args.copy,
                callback_function=args.callback_function))

        if len(args.sort_video_extentions):
            obj_sort.append(SortVideoFiles(
                path_root_src=args.path_root_src,
                path_root_dst=args.path_root_dst,
                ext_src=args.sort_video_extentions,
                delimiter=args.delimiter,
                subdir=(
                    args.subdir_year,
                    args.subdir_month),
                is_copy=args.copy,
                callback_function=args.callback_function))

        for obj in obj_sort:
            obj.sort_files()

    except Exception as err:
        traceback.print_exc()
        sys.exit(1)

    finally:
        pass
