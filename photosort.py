#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,glob,sys,string,re,time
import shutil
import argparse
import mediainfo
import traceback, logging
from exifread import process_file, __version__

TAG_DATE_TIME = 'EXIF DateTimeOriginal'

class SortFiles(object):
    def __init__(self, path_root_src='', path_root_dst='', ext_src=(), delimiter=''):
        extentions = []
        for extention in ext_src:
            extentions.append(extention.lower())
            extentions.append(extention.upper())
        
        setattr(self, "_ext_src", extentions)
        setattr(self, "_path_root_src", path_root_src)
        setattr(self, "_path_root_dst", path_root_dst)
        setattr(self, "_delimiter", delimiter)

        logging.debug(self._ext_src)
        logging.debug(self._path_root_src)
        logging.debug(self._path_root_dst)
        logging.debug(self._delimiter)
    
    def get_src_dir(self):
        return self._path_root_src
    
    def get_dst_dir(self):
        return self._path_root_dst
    
    def get_src_ext(self):
        return self._ext_src
    
    def get_delimiter(self):
        return self._delimiter
    
    def get_date_of_file(self, path_file_src):
        epoc_time = os.stat(path_file_src)
        mtime = time.gmtime(epoc_time.st_mtime)
        date = '{year:04d}-{month:02d}-{day:02d}'.format(year=mtime.tm_year, month=mtime.tm_mon, day=mtime.tm_mday)
        logging.debug('{file_src} has {mtime}.'.format(file_src=path_file_src, mtime=mtime))
        return date
    
    def sort_files(self):
        for extention in self._ext_src:
            pattern_search = '*.%s' % extention
            for path_src_img in glob.glob(os.path.join(self._path_root_src, pattern_search)):
                if not os.path.isfile(path_src_img):
                    continue
                
                try:
                    # get date directory name from specified file.
                    date = self.get_date_of_file(path_src_img)
                    date = date.replace('-', self._delimiter)
                    
                    logging.debug("date is %s." + date)
                    
                    # if destination path is not set, destination is same as source.
                    if len(self._path_root_dst) is not 0:
                        path_dst_dir = os.path.join(self._path_root_dst, date)
                    else:
                        path_dst_dir = os.path.join(os.path.dirname(path_src_img), date)
                    path_dst_img = os.path.join(path_dst_dir, os.path.basename(path_src_img))
                    
                    logging.debug("path_src_img is %s." % (path_src_img))
                    logging.debug("path_dst_img is %s." % (path_dst_img))
                    
                    logging.info("move \"%s\" to \"%s\"." % (path_src_img, path_dst_img))
                    
                    # create directory to move.
                    if not os.path.isdir(path_dst_dir):
                        os.mkdir(path_dst_dir)
                    shutil.move(path_src_img, path_dst_img)
                    
                except Exception as err:
                    logging.debug(str(type(err)) + " occurs with message \"" + err.message + "\".")
                    continue
                
                finally:
                    pass
    
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
                default='', \
                type=str, \
                choices=None, \
                help='Directory path where you want to create date folder and locate photo files. (default: same as source directory)', \
                metavar=None)
        parser.add_argument('-p', '--sort-photo-extentions', \
                action='store', \
                nargs='+', \
                const=None, \
                default=(), \
                type=str, \
                choices=None, \
                help='Extentions of photo file which you want to sort. (default: jpg)', \
                metavar=None)
        parser.add_argument('-v', '--sort-video-extentions', \
                action='store', \
                nargs='+', \
                const=None, \
                default=(), \
                type=str, \
                choices=None, \
                help='Extentions of video file which you want to sort. (default: jpg)', \
                metavar=None)
        parser.add_argument('-l', '--delimiter', \
                action='store', \
                nargs='?', \
                const='', \
                default='', \
                type=str, \
                choices=None, \
                help='A character as delimiter which you want to set the name of date folder like "2014-05-01". (default: none)', \
                metavar=None)
        parser.add_argument('--debug', \
                action='store', \
                default='info', \
                required=False, \
                help='debug mode if this flag is set (default: info)')
        args = parser.parse_args()

        obj_sort = []
        if len(args.sort_photo_extentions) > 0:
            obj_sort.append(SortPhotoFiles(args.path_root_src, \
                    args.path_root_dst, \
                    args.sort_photo_extentions, \
                    args.delimiter))
        if len(args.sort_video_extentions) > 0:
            obj_sort.append(SortVideoFiles(args.path_root_src, \
                    args.path_root_dst, \
                    args.sort_video_extentions, \
                    args.delimiter))
        
        for obj in obj_sort:
            obj.sort_files()
        
    except Exception as err:
        logging.debug("Exception type is " + type(err))
        logging.debug("Exception arg is " + err.args)
        logging.debug("Exception is " + err)
        
    finally:
        pass
