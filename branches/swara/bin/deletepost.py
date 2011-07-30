#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import sys,os
sys.path.append("/opt/swara/libs")
from utilities import *
from database import *
if __name__=="__main__":
	db = Database()
	post = sys.argv[1]
	db.deletePost(post)
	print ("Deleted post %s" %post)
