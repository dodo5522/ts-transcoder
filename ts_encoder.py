#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,platform,sys,re
import fcntl
import time

class ExecTool(object):
	pass

class ExecTsSplitter(ExecTool):
	pass

class ExecCciConv(ExecTool):
	pass

class ExecMediaCoder(ExecTool):
	pass

class ExecTrashBox(ExecTool):
	pass

if __name__ == '__main__':
	
	if platform.system() == 'Windows':
		pass
	else:
		# only for test on posix system
		fd = open('ts_encoder.lock', 'w')
		fcntl.flock(fd, fcntl.LOCK_EX)
		for count in range(0,5):
			time.sleep(1)
			print 'waiting... (%s)' % (count)
		fd.close()
	
	pass
