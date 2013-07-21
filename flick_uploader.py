#!/usr/bin/python
"""
	module: flick_uploader
	
	This script to upload media files to flickr.
	
	argument 1 : Local directory path including media files
	argument 2 : none
"""

import os,sys,string,re
import flickr_api as flickr
import pyexiv2 as exiv

ARGVS = sys.argv
ARGC = len(ARGVS)
FILE_OWN = ARGVS[0]

###################
# sub routine
###################
def LoadConfiguration():
	
	# conf file is based on py script name	
	PATH_FILE_CONF = re.sub(r'(.*).py', r'\1.conf', FILE_OWN)
	fp_conf = open(PATH_FILE_CONF, 'r')
	
	# read configuration	
	conf = dict()
	for read_line in fp_conf:
		line = string.strip(read_line)
		if line[0:len('API_KEY')] == 'API_KEY':
			conf['API_KEY'] = re.sub(r'API_KEY=([0-9a-z]+)', r'\1', line)
		elif line[0:len('API_SEC')] == 'API_SEC':
			conf['API_SEC'] = re.sub(r'API_SEC=([0-9a-z]+)', r'\1', line)
		elif line[0:len('URL_CALLBACK')] == 'URL_CALLBACK':
			conf['URL_CALLBACK'] = re.sub(r'URL_CALLBACK=(http://.+)', r'\1', line)
	fp_conf.close()
	
	# dump the configuration
	for key in conf.keys():
		print key + ' : ' + conf[key]
	
	return (conf['API_KEY'], conf['API_SEC'], conf['URL_CALLBACK'])

def LoadTokenFileOrGenerateItIfNotExists(api_key=None, api_sec=None, url_callback=None):
	
	if api_key == None or api_sec == None or url_callback == None:
		print 'Error: api_key(%s) or another is not specified.' % (api_key)
		return None
	
	PATH_FILE_TOKEN = re.sub(r'(.*).py', r'\1.token', FILE_OWN)
	
	# create object to authenticate
	flickr.set_keys(api_key, api_sec)
	
	if os.path.exists(PATH_FILE_TOKEN):
		print '%s already exists so load it.' % (PATH_FILE_TOKEN)
		auth = flickr.auth.AuthHandler.load(PATH_FILE_TOKEN)
	else:
		print '%s does not exist.' % (PATH_FILE_TOKEN)
		
		# set URL to get the query of oauth_token & oauth_verifier
		auth = flickr.auth.AuthHandler(callback=url_callback)
		
		# get URL for oauth
		url = auth.get_authorization_url('write')
		print url
		
		# store the token already verified
		verifier = raw_input('Enter the verifier:')
		auth.set_verifier(verifier)
		auth.save(PATH_FILE_TOKEN)
	
	# set the AuthHandler for the session
	flickr.set_auth_handler(auth)
	
	return flickr

def DumpMetaDataOfImage(path_file_media=None):
	if path_file_media is None:
		return False
	
	# get Meta data of jpeg file
	meta = exiv.ImageMetadata(path_file_media)
	meta.read()
	
	#for x in meta.xmp_keys:
	#        print x
	#
	#Xmp.dc.title
	#Xmp.dc.subject
	#...
	
	# only for debug
	for x in meta.xmp_keys:
		print x
	
	# tags
	meta['Xmp.dc.subject'].value[0]
	
	# title
	meta['Xmp.dc.title'].value['x-default']
	
	#for x in meta.xmp_keys:
	#        print x
	#
	#Iptc.Application2.ObjectName
	#Iptc.Application2.Keywords
	#...
	
	# tags
	meta['Iptc.Application2.ObjectName'].value[0]
	
	# title
	meta['Iptc.Application2.Keywords'].value[0]

###################
# main routine
###################

try:
	PATH_FILE_MEDIA = ARGVS[1]
	
	print 'Dump meta data of %s' % PATH_FILE_MEDIA
	DumpMetaDataOfImage(PATH_FILE_MEDIA)
	
	# load configuration file and get some parameters
	(API_KEY, API_SEC, URL_CALLBACK) = LoadConfiguration()
	
	# initialize flickr_api object
	obj = LoadTokenFileOrGenerateItIfNotExists(api_key=API_KEY,
	                                           api_sec=API_SEC,
	                                           url_callback=URL_CALLBACK)
	
	if obj != None and len(PATH_FILE_MEDIA) != 0:
		print 'Uploading media file '+PATH_FILE_MEDIA+'...'
		obj.upload(photo_file=PATH_FILE_MEDIA)
	else:
		print 'Upload error.'

except Exception as err:
	print 'Error type is '+str(type(err))+', '+str(err.args)+'.'

