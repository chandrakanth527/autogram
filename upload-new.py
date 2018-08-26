#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import os
import time
import random
from os import listdir
from os.path import isfile, join
from InstagramAPI import InstagramAPI
import urllib2
import urllib
import sys
import json
from PIL import Image, ImageDraw, ImageFont
import commands
import re

ID=sys.argv[1]

crontab=open("/root/instagram/crontab-ui/crontabs/crontab.db", "r")

for line in crontab:
    if re.match("(.*)"+ID+"(.*)", line):
       COMMANDARG=line

COMMANDSPLIT=json.loads(COMMANDARG)['command'].split("<break>")
IGUSER    =  COMMANDSPLIT[0] 
PASSWD=  COMMANDSPLIT[1] 
CAPTION=  COMMANDSPLIT[2] 
PROXY=  COMMANDSPLIT[3] 

igapi = InstagramAPI(IGUSER,PASSWD)
if PROXY != "":
   igapi.setProxy("http://"+PROXY)

igapi.login() # login
os.chdir("/root/instagram/")
 
TEMPFILEPREFIX=IGUSER

while True:
	igapi.getLikedMedia("")
	output=json.dumps(igapi.LastJson);
	jsonoutput=json.loads(output)
	instagramid=jsonoutput['items'][0]['code']
	mediaid=jsonoutput['items'][0]['id']
	igapi.unlike(mediaid)
	username=jsonoutput['items'][0]['user']['username'].encode('utf-8')
	CAPTIONNEW=CAPTION.replace("<username>","@"+username).replace("<newline>","\n")
	try:
		imageurl=jsonoutput['items'][0]['carousel_media'][0]['image_versions2']['candidates'][0]['url']
	except KeyError:
		imageurl=jsonoutput['items'][0]['image_versions2']['candidates'][0]['url']

	urllib.urlretrieve(imageurl, TEMPFILEPREFIX+"temp.jpg")
	try:
		videourl=jsonoutput['items'][0]['video_versions'][0]['url']
		commands.getstatusoutput("wget "+videourl+" -O " +TEMPFILEPREFIX+"temp.mp4")
   		igapi.uploadVideo(TEMPFILEPREFIX+"temp.mp4",TEMPFILEPREFIX+"temp.jpg",caption=CAPTIONNEW)
		if igapi.LastJson['status']=="ok":
			break
	
	except KeyError:
		videourl=""
   		igapi.uploadPhoto(TEMPFILEPREFIX+"temp.jpg",caption=CAPTIONNEW,upload_id=None)
		print igapi.LastJson['status']
		if igapi.LastJson['status']=="ok":
                        break	


