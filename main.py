#!/usr/bin/python

import flickr
import random
import urllib
import sys
import pywapi
import time

loc_codes = {'kolkata':'INXX0300', 'delhi':'INX0096', 'mumbai':'INX0087', 'chennai':'INXX0202', 'bangalore':'INXX0012'} 

def get_urls(tags):
	"""
	parameters = tags: string delimted by comma.
	returns the urls which contains those tags
	"""
	photos = flickr.photos_search(tags=tags)
	urls = []
	for photo in photos:
		urls.append('https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % (photo.farm, photo.server, photo.id, photo.secret))
	return urls

def download_image(urls):
	"""
	picks a random url and downloads and saves it in the current directory
	returns the file name of the image
	"""
	n = len(urls)
	idx = int(random.random() * n)	
	url = urls[idx]
	path = str(idx)+".jpg"
	urllib.urlretrieve(url, path)
	return path
	
def get_time_tags():
	"""
	Returns the relevant tags based on the time
	"""
	tags = None
	t = time.localtime()
	if (t.tm_hour >= 20 and t.tm_hour <= 23) or (t.tm_hour >= 0 and t.tm_hour <= 4):
		tag = 'night,starry,stars,moon'
	elif t.tm_hour >= 16 and t.tm_hour <= 19: 
		tag = 'evening,dusk,sunset'
	elif t.tm_hour >= 10 and t.tm_hour <= 15:
		tag = 'morning,noon'
	else:
		tag = 'dawn,sunrise'

	return tag

if __name__ == '__main__':

	l = sys.argv
	loc = l[1].lower()
	print "You selected location " + loc 
	if loc in loc_codes.keys():
		weather = pywapi.get_weather_from_yahoo(loc_codes[loc])
		weather_tags = [get_time_tags(),weather['condition']['text']]
		l = ','.join(weather_tags + l[2:])
		#print l
		urls = get_urls(l)

		#print download_image(urls)
	else:
		print "Invalid location! please select one of these locations: " + ', '.join(loc_codes.keys())


