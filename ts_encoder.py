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
	
	def execute(self, path_input='', path_output=''):
		'''
		Execute program with lock.
		'''
		cmd = self._generate_command(path_input, path_output)
		
		self._lock()
		
		print '"%s" runs with lock file "%s".' % (cmd, self._get_lock_name())
		subp = subprocess.Popen(cmd, \
				shell=True, \
				stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE)
		(data_stdout, data_stderr) = subp.communicate()
		path_output = self._suffix_execute(data_stdout, data_stderr)
		
		self._unlock()
		
		return path_output
	
	def _generate_command(self, path_input, path_output):
		'''
		Execute program before running execure() method.
		For example, generate command line string.
		'''
		return ''
	
	def _suffix_execute(self, data_stdout, data_stderr):
		'''
		Execute program after running execure() method.
		For example, generate path string to output target file.
		'''
		return ''

class ExecSplitTs(ExecTool):
	'''
	This is child class to execute TsSplitter tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_tssplitter.lock'
	
	def _generate_command(self, path_input, path_output):
		cmd = '{path_to_command} {option} {path_input}'.format(path_to_command=self._path_to_command, option='-SD -1SEG -WAIT2 -SEP3 -OVL5,7,0', path_input=path_input)
		return cmd
	
	def _suffix_execute(self, data_stdout, data_stderr):
		#FIXME:
		print 'remove TS files which has 1SEG and so on.'
		return ''

class ExecSyncAv(ExecTool):
	'''
	This is child class to execute cciconv tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_cciconv.lock'
	
	def _generate_command(self, path_input, path_output):
		cmd = '{path_to_command} {option} {path_input} {path_output}'.format(path_to_command=self._path_to_command, option='-er -c 0', path_input=path_input, path_output=path_output)
		return cmd
	
	def _suffix_execute(self, data_stdout, data_stderr):
		#FIXME:
		print 'rename and return the TS file which audio and video have been synched.'
		return ''

class ExecTranscode(ExecTool):
	'''
	This is child class to execute MediaCoder tool with exclusive.
	'''
	def _get_lock_name(self):
		return 'ts_encoder_mediacoder.lock'
	
	def _generate_command(self, path_input, path_output):
		cmd = '{path_to_command} {option} {preset} {path_input}'.format(path_to_command=self._path_to_command, option='-start -exit -preset', preset=self._path_to_config, path_input=path_input)
		return cmd
	
	def _suffix_execute(self, data_stdout, data_stderr):
		#FIXME:
		print 'revert to original TS file name and return the output TS file path.'
		return ''

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
	
	def _generate_command(self, path_input, path_output):
		cmd = '{path_to_command} {path_input}'.format(path_to_command=self._path_to_command, path_input=path_input)
		return cmd

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
	pass_to_next = args.path_to_ts_file
	
	for obj in objs:
		pass_to_next = obj.execute(pass_to_next)

if __name__ == '__main__':
	main()
