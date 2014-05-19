#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,platform,sys,re
import time
import argparse

if platform.system() == 'Windows':
	#FIXME:
	pass
else:
	import fcntl

class ExecTool(object):
	'''
	This is parent class to execute some tool with exclusive.
	'''
	def __init__(self):
		'''
		Initialize ExecTool class object.
		Create mutex like object, etc.
		'''
		fd = open(self._get_lock_name(), 'w')
		setattr(self, '_fd', fd)

	def __del__(self):
		'''
		Remove ExecTool class object.
		'''
		self._fd.close()
		self._fd = None

	def _get_lock_name(self):
		return 'default'

	def _lock(self):
		'''
		Lock mutex like object.
		'''
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			print self._fd
			fcntl.flock(self._fd, fcntl.LOCK_EX)

	def _unlock(self):
		'''
		Release mutex like object.
		'''
		if platform.system() == 'Windows':
			#FIXME:CreateMutex is needed on windows platform.
			pass
		else:
			print self._fd
			fcntl.flock(self._fd, fcntl.LOCK_UN)

	def execute(self):
		'''
		Execute program with lock.
		'''
		self._lock()
		for count in range(0,5):
			time.sleep(1)
			print '%s ... (%s)' % (self._get_lock_name(), count)
		self._unlock()

class ExecTsSplitter(ExecTool):
	'''
	This is child class to execute TsSplitter tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'

class ExecCciConv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'

class ExecMediaCoder(ExecTool):
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

if __name__ == '__main__':
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
	objs.append(ExecTsSplitter())
	objs.append(ExecCciConv())
	if args.skip == False:
		objs.append(ExecMediaCoder())
	objs.append(ExecTrashBox())
	
	for obj in objs:
		obj.execute()
