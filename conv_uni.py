#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import platform
import unicodedata


def str_to_uni(string):
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
    unicode_string = string.decode(system_encoding)
    return unicodedata.normalize(target_form, unicode_string)


def strs_to_unis(strings):
    for string in strings:
        yield str_to_uni(string)
