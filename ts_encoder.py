#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,platform,sys,re,glob
import shutil
import time
import argparse
import subprocess
import string,random

if platform.system() == 'Windows':
	#FIXME:
	pass
else:
	import fcntl

class ExecTool(object):
	def __init__(self, debug=False, path_to_command='', path_to_config=''):
		fd = open(self._get_lock_name(), 'w')
		setattr(self, '_fd_lock', fd)
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
		self._fd_lock.close()
		self._fd_lock = None
		os.remove(self._get_lock_name())
	
	def _get_lock_name(self):
		pass
	
	def _lock(self):
		if self._debug == True:
			print 'locking with ' + self._get_lock_name()
		
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			fcntl.flock(self._fd_lock, fcntl.LOCK_EX)
	
	def _unlock(self):
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			fcntl.flock(self._fd_lock, fcntl.LOCK_UN)
		
		if self._debug == True:
			print 'unlocked with ' + self._get_lock_name()
	
	def execute(self, path_input='', path_output=''):
		self._path_to_file_input = path_input
		self._path_to_file_output = path_output
		
		self._lock()
		self._execute_before()
		
		if self._debug == True:
			print '"%s" runs with lock file "%s".' % (self._cmdline, self._get_lock_name())
		
		subp = subprocess.Popen(self._cmdline, \
				shell=True, \
				stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE)
		(self._data_stdout, self._data_stderr) = subp.communicate()
		self._returncode = subp.returncode
		
		self._execute_after()
		self._unlock()
		
		return path_output
	
	def _execute_before(self):
		pass
	
	def _execute_after(self):
		pass

class ExecSplitTs(ExecTool):
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'
	
	def _execute_before(self):
		if self._debug == True:
			(base, ext) = os.path.splitext(self._path_to_file_input)
			pattern = '{cmd1}; {cmd2}; {cmd3}'
			self._cmdline = pattern.format(\
					cmd1 = 'echo "a" > ' + base + '_HD' + ext, \
					cmd2 = 'echo "cccccc" > ' + base + '_HD1' + ext, \
					cmd3 = 'echo "bbb" > ' + base + '_HD2' + ext)
		else:
			pattern = '{path_to_command} {option} {path_input}'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-SD -1SEG -WAIT2 -SEP3 -OVL5,7,0', \
					path_input=self._path_to_file_input)
	
	def _execute_after(self):
		dir_name = os.path.dirname(self._path_to_file_input)
		(base, ext) = os.path.splitext(os.path.basename(self._path_to_file_input))
		
		pattern = os.path.join(dir_name, base + '_HD*' + ext)
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
		
		if self._debug == True:
			print 'max size file is {file_max} with {size_max} bytes.'.format(file_max=files[index_size_max], size_max=size_max)
		
		shutil.move(files[index_size_max], self._path_to_file_output)
		
		if self._returncode != 0:
			print self._data_stderr

class ExecSyncAv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'
	
	def _execute_before(self):
		if self._debug == True:
			pattern = 'cp {file_input} {file_output}'
			self._cmdline = pattern.format(\
					file_input = self._path_to_file_input, \
					file_output = self._path_to_file_output)
		else:
			pattern = '{path_to_command} {option} {path_input} {path_output}'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-er -c 0', \
					path_input=self._path_to_file_input, \
					path_output=self._path_to_file_output)
	
	def _execute_after(self):
		os.remove(self._path_to_file_input)
		if self._returncode != 0:
			print self._data_stderr

class ExecTranscode(ExecTool):
	def __init__(self, debug=False, path_to_command='', path_to_config=''):
		ExecTool.__init__(self, debug, path_to_command, path_to_config)
		setattr(self, '_path_to_file_rand', '')
	
	def _get_lock_name(self):
		return 'ts_encoder_mediacoder.lock'
	
	def _execute_before(self):
		seed = string.digits + string.letters
		file_rand = 'rand'
		for i in range(0,9):
			file_rand += random.choice(seed)
		
		self._path_to_file_rand = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.ts')
		shutil.move(self._path_to_file_input, self._path_to_file_rand)
		
		if self._debug == True:
			pattern = 'cp {file_input} {file_output}'
			self._cmdline = pattern.format(\
					file_input = self._path_to_file_rand, \
					file_output = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.mp4'))
		else:
			pattern = '{path_to_command} {option} -preset {preset} {path_input}'
			self._cmdline = pattern.format(\
					path_to_command=self._path_to_command, \
					option='-start -exit', \
					preset=self._path_to_config, \
					path_input=self._path_to_file_rand)
	
	def _execute_after(self):
		#FIXME:
		print 'revert to mp4 file name and return the output TS file path.'
		if self._returncode != 0:
			print self._data_stderr

class ExecTrashBox(ExecTool):
	def _get_lock_name(self):
		return 'ts_encoder_trashbox.lock'
	
	def _lock(self):
		if self._debug == True:
			print "Don't need to lock/unlock for trashing ts file."
	
	def _unlock(self):
		if self._debug == True:
			print "Don't need to lock/unlock for trashing ts file."
	
	def _execute_before(self):
		pattern = '{path_to_command} {path_input}'
		self._cmdline = pattern.format(\
				path_to_command=self._path_to_command, \
				path_input=self._path_to_file_input)
	
	def _execute_after(self):
		if self._returncode != 0:
			print self._data_stderr

def main():
	# argument parsing process.
	parser = argparse.ArgumentParser(description='This script is to encode TS file recorded by PT2.')
	parser.add_argument('path_to_ts_file', \
			action='store', \
			default=None, \
			help='path to TS file.')
	parser.add_argument('-ts', '--tssplitter-path', \
			action='store', \
			default=None, \
			required=True, \
			help='command path to tssplitter.')
	parser.add_argument('-cc', '--cciconv-path', \
			action='store', \
			default=None, \
			required=True, \
			help='command path to cciconv.')
	parser.add_argument('-tb', '--trashbox-path', \
			action='store', \
			default=None, \
			required=True, \
			help='command path to trashbox.')
	parser.add_argument('-mc', '--mediacoder-path', \
			action='store', \
			default=None, \
			required=True, \
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
	args = parser.parse_args()
	
	# run the main operation
	objs = []
	objs.append(ExecSplitTs(args.debug, args.tssplitter_path))
	objs.append(ExecSyncAv(args.debug, args.cciconv_path))
	objs.append(ExecTranscode(args.debug, args.mediacoder_path, args.mediacoder_conf_path))
	objs.append(ExecTrashBox(args.debug, args.trashbox_path))
	path_input = args.path_to_ts_file
	
	for obj in objs:
		(base, ext) = os.path.splitext(path_input)
		path_output = base + '_' + ext
		obj.execute(path_input, path_output)
		path_input = path_output

if __name__ == '__main__':
	main()
