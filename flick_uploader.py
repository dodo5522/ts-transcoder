#!/usr/bin/python

'''
Upload media files to flickr.

 arg1 : Local directory path including media files
 arg2 : none
'''

import os
import sys
import flickr_api as flickr

# API key
API_KEY=''
API_SEC=''
PATH_FILE_TOKEN=''
URL_CALLBACK=''

API_KEY='68846c05f5861c882ebe1d53a96e985b'
API_SEC='614b4942cf70afe9'
PATH_FILE_TOKEN='/home/takashi/flickr_api_auth_token'
URL_CALLBACK='http://www.flickr.com/photos/98824049@N05/'

###################
# sub routine
###################
def LoadConfiguration():
	argvs = sys.argv
	argc = len(argvs)
	
	print argvs
	print argc
	
	
	
	print API_KEY
	print API_SEC
	print PATH_FILE_TOKEN
	print URL_CALLBACK
	sys.exit()
	return (API_KEY, API_SEC, PATH_FILE_TOKEN, URL_CALLBACK)

def LoadTokenFileOrGenerateItIfNotExists(path_auth_file=None, api_key=None, api_sec=None, url_callback=None):
	if api_key == None or api_sec == None or url_callback == None:
		print 'Error: api_key(%s) or another is not specified.' % (api_key)
		return None
	
	if path_auth_file == None:
		print 'Error: path_auth_file(%s) is invalid.' % (path_auth_file)
		return None
	
	# create object to authenticate
	flickr.set_keys(api_key, api_sec)
	
	if os.path.exists(path_auth_file):
		print '%s already exists so load it.' % (path_auth_file)
		auth = flickr.auth.AuthHandler.load(path_auth_file)
	else:
		print '%s does not exist.' % (path_auth_file)
		
		# set URL to get the query of oauth_token & oauth_verifier
		auth = flickr.auth.AuthHandler(callback=url_callback)
		
		# get URL for oauth
		url = auth.get_authorization_url('write')
		print url
		
		# store the token already verified
		verifier = raw_input('Enter the verifier:')
		auth.set_verifier(verifier)
		auth.save(path_auth_file)
	
	# set the AuthHandler for the session
	flickr.set_auth_handler(auth)
	
	return flickr

###################
# main routine
###################

# load configuration file and get some parameters
#(API_KEY, API_SEC, PATH_FILE_TOKEN, URL_CALLBACK) = LoadConfiguration()

# initialize flickr_api object
obj = LoadTokenFileOrGenerateItIfNotExists(path_auth_file=PATH_FILE_TOKEN,
                                           api_key=API_KEY,
                                           api_sec=API_SEC,
                                           url_callback=URL_CALLBACK)

if obj != None:
        # upload file
        obj.upload(photo_file='/home/takashi/DSC_0593.jpg')
else:
        print 'Error: auth is empty.'
        sys.exit()


