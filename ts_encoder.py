#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,platform,sys,re
import time
import argparse
import subprocess

if platform.system() == 'Windows':
	#FIXME:
	pass
else:
	import fcntl

class ExecTool(object):
	'''
	This is parent class to execute some tool with exclusive.
	'''
	def __init__(self, path_to_command='', path_to_config=''):
		'''
		Initialize ExecTool class object.
		Create mutex like object, etc.
		'''
		fd = open(self._get_lock_name(), 'w')
		setattr(self, '_fd_lock', fd)
		setattr(self, '_path_to_command', path_to_command)
		setattr(self, '_path_to_config', path_to_config)
		# belows are set by another method.
		setattr(self, '_path_to_file_input', '')
		setattr(self, '_path_to_file_output', '')
		setattr(self, '_cmdline', '')
		setattr(self, '_data_stdout', '')
		setattr(self, '_data_stderr', '')
		setattr(self, '_returncode', 0)
	
	def __del__(self):
		'''
		Remove ExecTool class object.
		'''
		self._fd_lock.close()
		self._fd_lock = None
		os.remove(self._get_lock_name())
	
	def _get_lock_name(self):
		pass
	
	def _lock(self):
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
		
		print 'unlocked with ' + self._get_lock_name()
	
	def execute(self, path_input='', path_output=''):
		'''
		Execute program with lock.
		'''
		
		self._path_to_file_input = path_input
		self._path_to_file_output = path_output
		
		self._lock()
		self._execute_before()
		
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
		'''
		Execute program before running execure() method.
		For example, generate command line string.
		'''
		pass
	
	def _execute_after(self):
		'''
		Execute program after running execure() method.
		For example, generate path string to output target file.
		'''
		pass

class ExecSplitTs(ExecTool):
	'''
	This is child class to execute TsSplitter tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'
	
	def _execute_before(self):
		self._cmdline = '{path_to_command} {option} {path_input}'.format(path_to_command=self._path_to_command, option='-SD -1SEG -WAIT2 -SEP3 -OVL5,7,0', path_input=self._path_to_file_input)
	
	def _execute_after(self):
		#FIXME:
		print 'remove TS files which has 1SEG and so on.'
		if self._returncode != 0:
			print self._data_stderr

class ExecSyncAv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'
	
	def _execute_before(self):
		self._cmdline = '{path_to_command} {option} {path_input} {path_output}'.format(path_to_command=self._path_to_command, option='-er -c 0', path_input=self._path_to_file_input, path_output=self._path_to_file_output)
	
	def _execute_after(self):
		#FIXME:
		print 'rename and return the TS file which audio and video have been synched.'
		if self._returncode != 0:
			print self._data_stderr

class ExecTranscode(ExecTool):
	'''
	This is child class to execute MediaCoder tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_mediacoder.lock'
	
	def _execute_before(self):
		#FIXME:
		print 'rename TS file to randomized file name to be used by media coder.'
		
		self._cmdline = '{path_to_command} {option} -preset {preset} {path_input}'.format(path_to_command=self._path_to_command, option='-start -exit', preset=self._path_to_config, path_input=self._path_to_file_input)
	
	def _execute_after(self):
		#FIXME:
		print 'revert to original TS file name and return the output TS file path.'
		if self._returncode != 0:
			print self._data_stderr

class ExecTrashBox(ExecTool):
	'''
	This is child class to execute trashbox tool without exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_trashbox.lock'
	
	def _lock(self):
		''' Don't need to lock/unlock for trashing ts file. '''
		pass
	
	def _unlock(self):
		''' Don't need to lock/unlock for trashing ts file. '''
		pass
	
	def _execute_before(self):
		self._cmdline = '{path_to_command} {path_input}'.format(path_to_command=self._path_to_command, path_input=self._path_to_file_input)
	
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
	objs.append(ExecSplitTs(args.tssplitter_path))
	objs.append(ExecSyncAv(args.cciconv_path))
	objs.append(ExecTranscode(args.mediacoder_path, args.mediacoder_conf_path))
	objs.append(ExecTrashBox(args.trashbox_path))
	path_input = args.path_to_ts_file
	
	for obj in objs:
		(base, ext) = os.path.splitext(path_input)
		path_output = base + '_' + ext
		obj.execute(path_input, path_output)
		path_input = path_output

if __name__ == '__main__':
	main()
