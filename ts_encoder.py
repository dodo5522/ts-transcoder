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
	def __init__(self, cmd):
		'''
		Initialize ExecTool class object.
		Create mutex like object, etc.
		'''
		fd = open(self._get_lock_name(), 'w')
		setattr(self, '_fd_lock', fd)
		setattr(self, '_cmd', cmd)

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
		
		print '%s is running with lock %s...' % (self._cmd, self._get_lock_name())
		subp = subprocess.Popen(self._cmd, \
				shell=True, \
				stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE)
		(data_stdout, data_stderr) = subp.communicate()
		
		self._unlock()

class ExecSplitTs(ExecTool):
	'''
	This is child class to execute TsSplitter tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'

class ExecSyncAv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'

class ExecTranscode(ExecTool):
	'''
	This is child class to execute MediaCoder tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_mediacoder.lock'

class ExecTrashBox(ExecTool):
	'''
	This is child class to execute trashbox tool without exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_trashbox.lock'

	def _lock(self):
		pass

	def _unlock(self):
		pass

def main():
	# argument parsing process.
	parser = argparse.ArgumentParser(description='This script is to encode TS file recorded by PT2.')
	parser.add_argument('--skip', \
			action='store_true', \
			default=False, \
			help='skip a process to test.')
	parser.add_argument('--debug', \
			action='store_true', \
			default=False, \
			help='debug mode.')
	args = parser.parse_args()
	
	# run the main operation
	objs = []
	objs.append(ExecSplitTs('ls -al'))
	objs.append(ExecSyncAv('mount'))
	if args.skip == False:
		objs.append(ExecTranscode('cat /etc/resolv.conf'))
	objs.append(ExecTrashBox('cat /etc/bashrc'))
	
	for obj in objs:
		obj.execute()

if __name__ == '__main__':
	main()
