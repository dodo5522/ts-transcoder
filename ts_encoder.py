#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os, platform, sys, re, glob, locale
import shutil
import time
import argparse
import subprocess
import string,random
import logging,traceback

if platform.system() == 'Windows':
    import win32mutex
else:
    import fcntl

class ExecTool(object):
    _path_to_file_origin = ''
    
    def __init__(self, stub=False, path_to_command='', path_to_config=''):
        if platform.system() == 'Windows':
            mutex = win32mutex.NamedMutex(self._get_lock_name(), False)
        else:
            mutex = open(self._get_lock_name(), 'w')
        setattr(self, '_mutex', mutex)
        setattr(self, '_path_to_command', path_to_command)
        setattr(self, '_path_to_config', path_to_config)
        setattr(self, '_stub', stub)
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
        ''' This method should be overrideddn by inherited class. '''
        return 'tool'
    
    def _get_lock_name(self):
        ''' This method should be overrideddn by inherited class. '''
        return 'ts_encoder_' + self._get_class_name() + '.lock'
    
    def _lock(self):
        logging.debug(u"entering mutex {lock_name}".format(lock_name=self._get_lock_name()))
        
        if platform.system() == 'Windows':
            self._mutex.acquire()
        else:
            fcntl.flock(self._mutex, fcntl.LOCK_EX)
        
        logging.debug(u"entered mutex {lock_name}".format(lock_name=self._get_lock_name()))
    
    def _unlock(self):
        logging.debug(u"exiting mutex {lock_name}".format(lock_name=self._get_lock_name()))
        
        if platform.system() == 'Windows':
            self._mutex.release()
        else:
            fcntl.flock(self._mutex, fcntl.LOCK_UN)
        
        logging.debug(u"exited mutex {lock_name}".format(lock_name=self._get_lock_name()))
    
    def execute(self, path_input=''):
        self._path_to_file_input = path_input
        
        self._lock()
        self._execute_before()
        
        logging.info(u'{cmd}'.format(cmd=self._cmdline))
        
        encoding = locale.getpreferredencoding()
        subp = subprocess.Popen(self._cmdline.encode(encoding), \
                shell=True, \
                stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        (self._data_stdout, self._data_stderr) = subp.communicate()
        self._returncode = subp.returncode
        
        self._execute_after()
        self._unlock()
        
        return self._path_to_file_output
    
    def _execute_before(self):
        ''' This method should be overrideddn by inherited class. '''
        pass
    
    def _execute_after(self):
        ''' This method should be overrideddn by inherited class. '''
        pass

class ExecSplitTs(ExecTool):
    def _get_class_name(self):
        return 'splitts'
    
    def _get_lock_name(self):
        return 'ts_encoder_' + self._get_class_name() + '.lock'
    
    def _execute_before(self):
        ExecTool._path_to_file_origin = self._path_to_file_input
        (base, ext) = os.path.splitext(self._path_to_file_input)
        self._path_to_file_output = base + '_' + self._get_class_name() + ext
        
        if self._stub == True:
            pattern = u'{cmd1}; {cmd2}; {cmd3}; {cmd4}'
            self._cmdline = pattern.format(\
                    cmd1 = u'echo "a" > ' + base + u'_HD' + ext, \
                    cmd2 = u'echo "cccccc" > ' + base + u'_HD1' + ext, \
                    cmd3 = u'echo "bbb" > ' + base + u'_HD2' + ext, \
                    cmd4 = u'echo "acccccbbb" > ' + ExecTool._path_to_file_origin)
        else:
            pattern = u'"{path_to_command}" {option} "{path_input}"'
            self._cmdline = pattern.format(\
                    path_to_command=self._path_to_command, \
                    option=u'-SD -1SEG -WAIT2 -SEP3 -OVL5,7,0', \
                    path_input=self._path_to_file_input)
    
    def _execute_after(self):
        (base, ext) = os.path.splitext(self._path_to_file_input)
        pattern = base + u'_HD*' + ext
        files = glob.glob(pattern)
        
        if self._returncode >= 0 and len(files) > 0:
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
            
            logging.debug(u'max is {file_max} {size_max} bytes.'.format(file_max=files[index_size_max], size_max=size_max))
            shutil.move(files[index_size_max], self._path_to_file_output)
            
            logging.info(u'{CLASS} success.'.format(CLASS=self._get_class_name()))
        else:
            logging.error(self._data_stderr)
            raise IOError('{CLASS} failed with return code {CODE} and length {LEN}!'.format(CLASS=self._get_class_name(), CODE=self._returncode, LEN=len(files)))

class ExecSyncAv(ExecTool):
    def _get_class_name(self):
        return 'syncav'
    
    def _get_lock_name(self):
        return 'ts_encoder_' + self._get_class_name() + '.lock'
    
    def _execute_before(self):
        (base, ext) = os.path.splitext(self._path_to_file_input)
        self._path_to_file_output = base + '_' + self._get_class_name() + ext
        
        if self._stub == True:
            pattern = u'cp {file_input} {file_output}'
            self._cmdline = pattern.format(\
                    file_input = self._path_to_file_input, \
                    file_output = self._path_to_file_output)
        else:
            pattern = u'"{path_to_command}" {option} "{path_input}" "{path_output}"'
            self._cmdline = pattern.format(\
                    path_to_command=self._path_to_command, \
                    option=u'-er -c 0', \
                    path_input=self._path_to_file_input, \
                    path_output=self._path_to_file_output)
    
    def _execute_after(self):
        os.remove(self._path_to_file_input)
        if self._returncode >= 0:
            logging.info(u'{CLASS} success.'.format(CLASS=self._get_class_name()))
        else:
            logging.error(self._data_stderr)
            raise IOError('{CLASS} failed!'.format(CLASS=self._get_class_name()))

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
        self._path_to_file_output = base + u'.mp4'
        
        seed = string.digits + string.letters
        file_rand = u'rand'
        for i in range(0,9):
            file_rand += random.choice(seed)
        
        # mediacoder can handle ASCII code file name, so move original TS file to randamized one.
        self._path_to_file_rand_ts = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.ts')
        shutil.move(self._path_to_file_input, self._path_to_file_rand_ts)
        
        if self._stub == True:
            pattern = u'cp {file_input} {file_output}'
            self._cmdline = pattern.format(\
                    file_input = self._path_to_file_rand_ts, \
                    file_output = os.path.join(os.path.dirname(self._path_to_file_input), file_rand + '.mp4'))
        else:
            pattern = u'"{path_to_command}" {option} -preset "{preset}" "{path_input}"'
            self._cmdline = pattern.format(\
                    path_to_command=self._path_to_command, \
                    option=u'-start -exit', \
                    preset=self._path_to_config, \
                    path_input=self._path_to_file_rand_ts)
    
    def _execute_after(self):
        (base, ext) = os.path.splitext(self._path_to_file_rand_ts)
        os.remove(self._path_to_file_rand_ts)
        if os.path.isfile(base + u'.mp4'):
            shutil.move(base + u'.mp4', self._path_to_file_output)
            logging.info(u'{CLASS} success.'.format(CLASS=self._get_class_name()))
        else:
            logging.error(self._data_stderr)
            raise IOError('{CLASS} failed!'.format(CLASS=self._get_class_name()))

class ExecTrashBox(ExecTool):
    def _get_class_name(self):
        return 'trash'
    
    def _get_lock_name(self):
        return 'ts_encoder_' + self._get_class_name() + '.lock'
    
    def _lock(self):
        logging.debug(u"Don't need to lock/unlock for trashing ts file.")
    
    def _unlock(self):
        logging.debug(u"Don't need to lock/unlock for trashing ts file.")
    
    def _execute_before(self):
        if self._stub == True:
            pattern = u'rm -f {path_input}'
            self._cmdline = pattern.format(\
                    path_input = ExecTool._path_to_file_origin)
        else:
            pattern = u'"{path_to_command}" "{path_input}"'
            self._cmdline = pattern.format(\
                    path_to_command=self._path_to_command, \
                    path_input = ExecTool._path_to_file_origin)
    
    def _execute_after(self):
        if self._returncode >= 0:
            logging.info(u'{CLASS} success.'.format(CLASS=self._get_class_name()))
        else:
            logging.error(self._data_stderr)
            raise IOError('{CLASS} failed!'.format(CLASS=self._get_class_name()))

