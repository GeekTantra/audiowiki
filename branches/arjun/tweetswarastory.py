#!/usr/bin/python

# Requires tweepy,simplejson and oauth0
# further requires a config file (tweetrswara.conf) with the access token for the swara user

import os,sys,time
from database import *
from utilities import *
import ConfigParser
import tweepy
import oauth2 as oauth
import os,sys

config=ConfigParser.ConfigParser()
config.read("/home/swara/audiowiki/twittercredsswara.conf")

OAUTH_TOKEN = config.get("Authentication","oauth_token")
OAUTH_TOKEN_SECRET = config.get("Authentication","oauth_token_secret")
CONSUMER_KEY = config.get("Consumer","consumer_key")
CONSUMER_SECRET = config.get("Consumer","consumer_secret")

#Create objects
auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

db = Database()    
api = tweepy.API(auth)

def getLastPushedPostID():
	post=os.popen("cat lastpushedpost").read().strip()
	return post

def tweet(post):
	title=db.getTitleforPost(12345,post)[0][:120]
	url="http://cgnetswara.org/index.php?id="+str(post)
	print title + " " + url
	status=title +" "+ url
	api.update_status(status)
	#debugPrint("Tweeted post %s" %post)

if __name__=="__main__":
	#Create Database object
   	postid=getLastPushedPostID() 
	print postid
	posts=db.getUnpushedPostsInChannel(12345,postid)
	if len(posts) == 0:
		print "No unpushed posts"
		exit()
	for post in posts:
		tweet(post)
	print "Final post = " + str(post)
	os.system("echo %s > lastpushedpost" %(str(post)))
