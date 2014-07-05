#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import platform
import unicodedata

def str_to_unicode(strings):
    if platform.system() == 'Windows':
        system_encoding = 'shift-jis'
        target_form = 'NFC'
    elif platform.system() == 'Darwin':
        system_encoding = 'utf-8'
        target_form = 'NFD'
    elif platform.system() == 'Linux':
        system_encoding = 'utf-8'
        target_form = 'NFC'
    else:
        raise SystemError('System platform is not defined.')

    for string in strings:
        unicode_string = string.decode(system_encoding)
        yield unicodedata.normalize(target_form, unicode_string)
