#!/usr/bin/python

import os
import subprocess
import xml.etree.ElementTree as et

class TrackInfo(object):
	def __init__(self, element_track=None):
		for child in element_track:
			setattr(self, child.tag, child.text)
	
	def get_format(self):
		if hasattr(self, 'Format'):
			return self.Format
		else:
			return None
	
	def get_encoded_date(self):
		if hasattr(self, 'Encoded_date'):
			return self.Encoded_date
		else:
			return None
	
	def get_duration(self):
		if hasattr(self, 'Duration'):
			return self.Duration
		else:
			return None
	
	def get_bit_rate(self):
		if hasattr(self, 'Bit_rate'):
			return self.Bit_rate
		else:
			return None

class GeneralInfo(TrackInfo):
	def get_model(self):
		if hasattr(self, 'Model'):
			return self.Model
		else:
			return None

class AudioInfo(TrackInfo):
	def get_channels(self):
		if hasattr(self, 'Channel_s_'):
			return self.Channel_s_
		else:
			return None

class VideoInfo(TrackInfo):
	def get_width(self):
		if hasattr(self, 'Width'):
			return self.Width
		else:
			return None
	
	def get_height(self):
		if hasattr(self, 'Height'):
			return self.Height
		else:
			return None
	
	def get_aspect_ratio(self):
		if hasattr(self, 'Display_aspect_ratio'):
			return self.Display_aspect_ratio
		else:
			return None
	
	def get_frame_rate(self):
		if hasattr(self, 'Frame_rate'):
			return self.Frame_rate
		else:
			return None
	
	def get_frame_rate_min(self):
		if hasattr(self, 'Minimum_frame_rate'):
			return self.Minimum_frame_rate
		else:
			return None
	
	def get_frame_rate_max(self):
		if hasattr(self, 'Maximum_frame_rate'):
			return self.Maximum_frame_rate
		else:
			return None

class MediaInfo(object):
	def __init__(self, path_xml):
		etree = et.parse(path_xml)
		
		eroot = etree.getroot()
		for key in eroot.attrib.keys():
			setattr(self, key, eroot.attrib[key])
		
		efile = None
		for child in eroot.getchildren():
			if 'File' in child.tag:
				# this class cannot have multiple file attribute.
				efile = child
				break
		
		for etrack in efile:
			attr = etrack.attrib
			if attr.has_key('type'):
				attr_type = attr['type']
			
			if attr_type == 'General':
				obj = GeneralInfo(etrack)
				setattr(self, "info_general", obj)
			elif attr_type == 'Audio':
				obj = AudioInfo(etrack)
				setattr(self, "info_audio", obj)
			elif attr_type == 'Video':
				obj = VideoInfo(etrack)
				setattr(self, "info_video", obj)
			else:
				pass

if __name__ == '__main__':
	try:
		obj = MediaInfo('mediainfo_sample_video.xml')
		pass
	except Exception as err:
		print err
	finally:
		pass
