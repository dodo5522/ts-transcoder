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
		'''
		Lock mutex like object.
		'''
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			print self._fd_lock
			fcntl.flock(self._fd_lock, fcntl.LOCK_EX)
	
	def _unlock(self):
		'''
		Release mutex like object.
		'''
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			print self._fd_lock
			fcntl.flock(self._fd_lock, fcntl.LOCK_UN)
	
	def execute(self):
		'''
		Execute program with lock.
		'''
		self._lock()
		self._prefix_execute()
		
		print '%s is running with lock %s...' % (self._cmd, self._get_lock_name())
		subp = subprocess.Popen(self._cmd, \
				shell=True, \
				stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE)
		(data_stdout, data_stderr) = subp.communicate()
		
		self._suffix_execute()
		self._unlock()
	
	def _prefix_execute(self):
		'''
		Execute program before running execure() method.
		'''
		pass
	
	def _suffix_execute(self):
		'''
		Execute program after running execure() method.
		'''
		pass

class ExecSplitTs(ExecTool):
	'''
	This is child class to execute TsSplitter tool with exclusive.
	'''
	def __init__(self):
		ExecTool.__init__(self, 'ls -al')
	
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'
	
	def _suffix_execute(self):
		#FIXME:
		print 'remove TS files which has 1SEG and so on.'
		pass

class ExecSyncAv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def __init__(self):
		ExecTool.__init__(self, 'mount')
	
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'
	
	def _suffix_execute(self):
		#FIXME:
		print 'rename TS file which audio and video have been synched.'
		pass

class ExecTranscode(ExecTool):
	'''
	This is child class to execute MediaCoder tool with exclusive.
	'''
	def __init__(self):
		ExecTool.__init__(self, 'cat /etc/resolv.conf')
	
	def _get_lock_name(self):
		return 'ts_encoder_mediacoder.lock'
	
	def _prefix_execute(self):
		#FIXME:
		print 'rename to some randomized TS file name for media coder.'
		pass
	
	def _suffix_execute(self):
		#FIXME:
		print 'revert to original TS file name.'
		pass

class ExecTrashBox(ExecTool):
	'''
	This is child class to execute trashbox tool without exclusive.
	'''
	def __init__(self):
		ExecTool.__init__(self, 'cat /etc/bashrc')
	
	def _get_lock_name(self):
		return 'ts_encoder_trashbox.lock'
	
	def _lock(self):
		''' Don't need to lock/unlock for trashing ts file. '''
		pass
	
	def _unlock(self):
		''' Don't need to lock/unlock for trashing ts file. '''
		pass

def main():
	# argument parsing process.
	parser = argparse.ArgumentParser(description='This script is to encode TS file recorded by PT2.')
	parser.add_argument('path_to_ts_file', \
			action='store', \
			default=None, \
			help='path to TS file.')
	parser.add_argument('--tssplitter-path', \
			action='store', \
			default=None, \
			help='command path to tssplitter.')
	parser.add_argument('--cciconv-path', \
			action='store', \
			default=None, \
			help='command path to cciconv.')
	parser.add_argument('--trashbox-path', \
			action='store', \
			default=None, \
			help='command path to trashbox.')
	parser.add_argument('--mediacoder-path', \
			action='store', \
			default=None, \
			help='command path to media coder.')
	parser.add_argument('--mediacoder-conf-path', \
			action='store', \
			default=None, \
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
	
	for obj in objs:
		obj.execute()

if __name__ == '__main__':
	main()
