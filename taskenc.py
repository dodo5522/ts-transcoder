#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os, argparse
import conv_uni
import automove
import logging, traceback
from ts_encoder import *

if __name__ == '__main__':
    # argument parsing process.
    parser = argparse.ArgumentParser(description='This script is to encode TS file recorded by PT2.')
    parser.add_argument('paths_to_ts_file', \
            nargs='+', \
            action='store', \
            default=None, \
            help='path to TS files.')
    parser.add_argument('-ts', '--tssplitter-path', \
            action='store', \
            default='C:\Program Files2\PT2\\taskenc\\3rdparty\TsSplitter\TsSplitter.exe', \
            required=False, \
            help='command path to tssplitter.')
    parser.add_argument('-cc', '--cciconv-path', \
            action='store', \
            default='C:\Program Files2\PT2\\taskenc\\3rdparty\cciconv\\release\win_x64\cciconv188.exe', \
            required=False, \
            help='command path to cciconv.')
    parser.add_argument('-tb', '--trashbox-path', \
            action='store', \
            default='C:\Program Files2\PT2\\taskenc\\3rdparty\GB\GB.exe', \
            required=False, \
            help='command path to trashbox.')
    parser.add_argument('-mc', '--mediacoder-path', \
            action='store', \
            default='C:\Program Files\MediaCoder\MediaCoder.exe', \
            required=False, \
            help='command path to media coder.')
    parser.add_argument('-mf', '--mediacoder-conf-path', \
            action='store', \
            default=None, \
            required=True, \
            help='configuration file for media coder.')
    parser.add_argument('-mv', '--path-target-to-move', \
            action='store', \
            default='F:\\videos\TV', \
            required=False, \
            help='path to move transcoded media file.')
    parser.add_argument('--stub', \
            action='store_true', \
            default=False, \
            help='stub mode.')
    parser.add_argument('--log-level', \
            action='store', \
            default='info', \
            required=False, \
            help='log level should be set as debug, info, warning, error, or critical.')
    parser.add_argument('--log-store-file', \
            action='store', \
            nargs='?', \
            default=None, \
            const=os.path.join(os.getcwd(), 'ts_encoder.log'), \
            required=False, \
            help='if this option is set, log data is stored into the specified file.')
    args = parser.parse_args()
    
    # set logging level at first
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if isinstance(numeric_level, int):
        logging.basicConfig(filename=args.log_store_file, level=numeric_level)
    
    # init object for media coder
    obj_execmc = ExecTranscode(\
            args.stub, \
            args.mediacoder_path, \
            args.mediacoder_conf_path)

    # run the main operation
    objs = []
    objs.append(ExecSplitTs(args.stub, args.tssplitter_path))
    objs.append(ExecSyncAv(args.stub, args.cciconv_path))
    objs.append(obj_execmc)
    objs.append(ExecTrashBox(args.stub, args.trashbox_path))
    
    for path_input in conv_uni.strs_to_unis(args.paths_to_ts_file):
        try:
            for obj in objs:
                path_output = obj.execute(path_input)
                path_input = path_output
        except Exception as err:
            traceback.print_exc()

    if args.path_target_to_move is not None:
        obj_automv = automove.AutoMove(conv_uni.str_to_uni(args.path_target_to_move))
        obj_automv.move(obj_execmc._path_to_file_output)

