#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,platform,sys,re,glob
import shutil
import time
import argparse
import subprocess
import string,random
import unittest,logging,traceback

if platform.system() == 'Windows':
	import win32mutex
else:
	import fcntl

class ExecTool(object):
	_path_to_file_origin = ''
	
	def __init__(self, debug=False, path_to_command='', path_to_config=''):
		if platform.system() == 'Windows':
			mutex = win32mutex.NamedMutex(self._get_lock_name(), False)
		else:
			mutex = open(self._get_lock_name(), 'w')
		setattr(self, '_mutex', mutex)
		setattr(self, '_path_to_command', path_to_command)
		setattr(self, '_path_to_config', path_to_config)
		setattr(self, '_debug', debug)
		# belows are set by another method.
		setattr(self, '_path_to_file_input', '')
		setattr(self, '_path_to_file_output', '')
		setattr(self, '_cmdline', '')
		setattr(self, '_data_stdout', '')
		setattr(self, '_data_stderr', '')
		setattr(self, '_returncode', 0)
	
	def __del__(self):
		self._mutex.close()
		if platform.system() == 'Windows':
			pass
		else:
			os.remove(self._get_lock_name())
		self._mutex = None
	
	def _get_class_name(self):
		return 'tool'
	
	def _get_lock_name(self):
		return 'ts_encoder_' + self._get_class_name() + '.lock'
	
	def _lock(self):
		logging.debug('locking with {lock_name}'.format(lock_name=self._get_lock_name()))
		
		if platform.system() == 'Windows':
			logging.debug("entering mutex {lock_name}".format(lock_name=self._get_lock_name()))
			self._mutex.acquire()
			logging.debug("entered mutex {lock_name}".format(lock_name=self._get_lock_name()))
		else:
			fcntl.flock(self._mutex, fcntl.LOCK_EX)
	
	def _unlock(self):
		if platform.system() == 'Windows':
			logging.debug("exiting mutex {lock_name}".format(lock_name=self._get_lock_name()))
			self._mutex.release()
			logging.debug("exited mutex {lock_name}".format(lock_name=self._get_lock_name()))
		else:
			fcntl.flock(self._mutex, fcntl.LOCK_UN)
		
		logging.debug('unlocked with {lock_name}'.format(lock_name=self._get_lock_name()))
	
	def execute(self, path_input=''):
		self._path_to_file_input = path_input
		
		self._lock()
		self._execute_before()
		
		logging.info('{cmd}'.format(cmd=self._cmdline))
		
		subp = subprocess.Popen(self._cmdline, \
				shell=True, \
				stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE)
		(self._data_stdout, self._data_stderr) = subp.communicate()
		self._returncode = subp.returncode
		
		self._execute_after()
		self._unlock()
		
		return self._path_to_file_output
	
	def _execute_before(self):
		# just for example
		(base, ext) = os.path.splitext(self._path_to_file_input)
		self._path_to_file_output = base + '_' + ext
	
	def _execute_after(self):
		# just for example
		(base, ext) = os.path.splitext(self._path_to_file_input)
		self._path_to_file_output = base + '_' + '.mp4'

class ExecSplitTs(ExecTool):
	def _get_class_name(self):
		return 'splitts'
	
	def _get_lock_name(self):
		return 'ts_encoder_' + self._get_class_name() + '.lock'
	
	def _execute_before(self):
		ExecTool._path_to_file_origin = self._path_to_file_input
		(base, ext) = os.path.splitext(self._path_to_file_input)
		self._path_to_file_output = base + '_' + self._get_class_name() + ext
		
		if self._debug == True:
			pattern = '{cmd1}; {cmd2}; {cmd3}; {cmd4}'
			self._cmdline = pattern.format(\
					cmd1 = 'echo "a" > ' + base + '_HD' + ext, \
					cmd2 = 'echo "cccccc" > ' + base + '_HD1' + ext, \
					cmd3 = 'echo "bbb" > ' + base + '_HD2' + ext, \
					cmd4 = 'echo "acccccbbb" > ' + ExecTool._path_to_file_origin)
		else:
			pattern = '"{path_to_command}" {option} "{path_input}"'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-SD -1SEG -WAIT2 -SEP3 -OVL5,7,0', \
					path_input=self._path_to_file_input)
	
	def _execute_after(self):
		(base, ext) = os.path.splitext(self._path_to_file_input)
		pattern = base + '_HD*' + ext
		files = glob.glob(pattern)
		
		size_max = 0
		index_size_max = 0
		for file_found in files:
			if size_max < os.path.getsize(file_found):
				size_max = os.path.getsize(file_found)
				index_size_max = files.index(file_found)
				if index_size_max > 0:
					file_remove = files[index_size_max - 1]
					os.remove(file_remove)
			else:
				os.remove(file_found)
		
		logging.debug('max size file is {file_max} with {size_max} bytes.'.format(file_max=files[index_size_max], size_max=size_max))
		
		shutil.move(files[index_size_max], self._path_to_file_output)
		
		if self._returncode != 0:
			logging.error(self._data_stderr)

class ExecSyncAv(ExecTool):
	def _get_class_name(self):
		return 'syncav'
	
	def _get_lock_name(self):
		return 'ts_encoder_' + self._get_class_name() + '.lock'
	
	def _execute_before(self):
		(base, ext) = os.path.splitext(self._path_to_file_input)
		self._path_to_file_output = base + '_' + self._get_class_name() + ext
		
		if self._debug == True:
			pattern = 'cp {file_input} {file_output}'
			self._cmdline = pattern.format(\
					file_input = self._path_to_file_input, \
					file_output = self._path_to_file_output)
		else:
			pattern = '"{path_to_command}" {option} "{path_input}" "{path_output}"'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-er -c 0', \
					path_input=self._path_to_file_input, \
					path_output=self._path_to_file_output)
	
	def _execute_after(self):
		os.remove(self._path_to_file_input)
		if self._returncode != 0:
			logging.error(self._data_stderr)

class ExecTranscode(ExecTool):
	def __init__(self, debug=False, path_to_command='', path_to_config=''):
		ExecTool.__init__(self, debug, path_to_command, path_to_config)
		setattr(self, '_path_to_file_rand_ts', '')
	
	def _get_class_name(self):
		return 'transcode'
	
	def _get_lock_name(self):
		return 'ts_encoder_' + self._get_class_name() + '.lock'
	
	def _execute_before(self):
		(base, ext) = os.path.splitext(self._path_to_file_origin)
		self._path_to_file_output = base + '.mp4'
		
		seed = string.digits + string.letters
		file_rand = 'rand'
		for i in range(0,9):
			file_rand += random.choice(seed)
		
		# mediacoder can handle ASCII code file name, so move original TS file to randamized one.
		self._path_to_file_rand_ts = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.ts')
		shutil.move(self._path_to_file_input, self._path_to_file_rand_ts)
		
		if self._debug == True:
			pattern = 'cp {file_input} {file_output}'
			self._cmdline = pattern.format(\
					file_input = self._path_to_file_rand_ts, \
					file_output = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.mp4'))
		else:
			pattern = '"{path_to_command}" {option} -preset "{preset}" "{path_input}"'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-start -exit', \
					preset=self._path_to_config, \
					path_input=self._path_to_file_rand_ts)
	
	def _execute_after(self):
		(base, ext) = os.path.splitext(self._path_to_file_rand_ts)
		shutil.move(base + '.mp4', self._path_to_file_output)
		os.remove(self._path_to_file_rand_ts)
		
		if self._returncode != 0:
			logging.error(self._data_stderr)

class ExecTrashBox(ExecTool):
	def _get_class_name(self):
		return 'trash'
	
	def _get_lock_name(self):
		return 'ts_encoder_' + self._get_class_name() + '.lock'
	
	def _lock(self):
		logging.debug("Don't need to lock/unlock for trashing ts file.")
	
	def _unlock(self):
		logging.debug("Don't need to lock/unlock for trashing ts file.")
	
	def _execute_before(self):
		if self._debug == True:
			pattern = 'rm -f {path_input}'
			self._cmdline = pattern.format(\
					path_input = ExecTool._path_to_file_origin)
		else:
			pattern = '"{path_to_command}" "{path_input}"'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					path_input = ExecTool._path_to_file_origin)
	
	def _execute_after(self):
		if self._returncode != 0:
			logging.error(self._data_stderr)

def main():
	# argument parsing process.
	parser = argparse.ArgumentParser(description='This script is to encode TS file recorded by PT2.')
	parser.add_argument('path_to_ts_file', \
			action='store', \
			default=None, \
			help='path to TS file.')
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
	parser.add_argument('--debug', \
			action='store_true', \
			default=False, \
			help='debug mode.')
	parser.add_argument('--log-level', \
			action='store', \
			default='info', \
			required=False, \
			help='log level should be set as debug, info, warning, error, or critical.')
	parser.add_argument('--log-store-file', \
			action='store', \
			nargs='?', \
			default=None, \
			const='ts_encoder.log', \
			required=False, \
			help='if this option is set, log data is stored into the specified file.')
	args = parser.parse_args()
	
	try:
		# set logging level at first
		numeric_level = getattr(logging, args.log_level.upper(), None)
		if not isinstance(numeric_level, int):
			raise ValueError('Invalid log level {log_level}'.format(log_level=args.log_level))
		logging.basicConfig(level=numeric_level)
		
		# run the main operation
		objs = []
		objs.append(ExecSplitTs(args.debug, args.tssplitter_path))
		objs.append(ExecSyncAv(args.debug, args.cciconv_path))
		objs.append(ExecTranscode(args.debug, args.mediacoder_path, args.mediacoder_conf_path))
		objs.append(ExecTrashBox(args.debug, args.trashbox_path))
		path_input = args.path_to_ts_file
		
		for obj in objs:
			path_output = obj.execute(path_input)
			path_input = path_output
		
	except Exception as err:
		traceback.print_exc()

if __name__ == '__main__':
	main()
