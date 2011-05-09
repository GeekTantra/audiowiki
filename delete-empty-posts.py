#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import sys,os
from utilities import *
from database import *
if __name__=="__main__":
	db = Database()
	list=os.popen("for i in `ls /home/swara/audiowiki/web/sounds/web/*.mp3`;do echo $i `mplayer -vo null -ao null -frames 0 -identify $i  2>/dev/null | grep ID_LENGTH | awk -F= '{print $2}'`;done").read().strip().split('\n')
	for line in list:
		lenpost=line.split(' ')[1]
		if float(lenpost) < 5:
			filename=line.split(' ')[0]
			post = filename.split("sounds/web/")[1].split('.')[0]
			db.deletePost(post)
			print ("Deleted short post %s length was %s" %(post,lenpost))
			os.system("rm %s" %filename)
