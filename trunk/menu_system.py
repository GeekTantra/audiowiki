#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import sys
if len(sys.argv) > 1:
    DEBUG = True
    if sys.argv[1] == 'auto':
        DEBUG_AUTO = True
    elif sys.argv[1] == 'man':
        DEBUG_AUTO = False
    else:
        print 'Usage: '+sys.argv[0]+' [auto|man]'
        print ''
        print 'Where no arguments implies the system is running in asterisk,'
        print 'auto runs the automated tests and man runs the keyboard-'
        print 'based manual testbed.'
else:
    DEBUG = False
    DEBUG_AUTO = False
        
import os
import re
import time
import random
import copy
from utilities import *
if DEBUG:
    if DEBUG_AUTO:
        from auto_mockasteriskinterface import *
    else:
        from mockasteriskinterface import *
else:
    from asteriskinterface import *
from database import *

SOUND_DIR = '/var/lib/asterisk/sounds/'

sys.setrecursionlimit(10000)

##### State functions ######

def login():
    """
    Implements the login state.

    If the user is here for the first time, plays the greeting and
    requires they create a personal greeting.

    Everyone hears the login message.
    """
    #if not db.isUser(user):
    #    playFile('first-time-message',{})
    #while not db.isUser(user):
    #    recordUserMessage()
    if not db.isUser(user):
        db.addContactedUser(user)
    playFile('login',{})

def mainMenu():
    """
    Implements the main menu state
    """
    keyDict = newKeyDict()
    keyDict['1'] = (RaiseKey,('1',))
    keyDict['2'] = (RaiseKey,('2',))
    keyDict['*'] = (RaiseKey,('*',))

    try:
        while True:
            category = walkCategoryTree('main-menu-intro', 'main-menu-outro',
                                        None, keyDict)
            if category != '0':
                break        
    except KeyPressException, e:
        if e.key == '1':
            recentThreads()
            return
        elif e.key == '2':
            popularThreads()
            return
        elif e.key == '*':
            personalOptions()
            return
        else:
            raise
    listThreads(category)
    
def recentThreads():
    threads = db.getRecentThreads(0,100)
    playThreadList(threads)
    
def popularThreads():
    threads = db.getPopularThreads()
    playThreadList(threads)

def listThreads(category):
    threads = db.getCategoryThreads(category)
    playThreadList(threads)

def playThreadList(threadList):
    if not threadList:
        playFile('empty-category')
        return
    while True:
        pageCount = int(len(threadList))/9 + 1
        debugPrint(str(pageCount))
        for i in xrange(pageCount):
            currentKey = 1    
            keyDict = newKeyDict()
            for thread in threadList[(i*9):((i+1)*9)]:
                keyDict[str(currentKey)] = (readThread,(thread,))
                currentKey+=1

            currentKey = 1
            for thread in threadList[(i*9):((i+1)*9)]:
                playThread(thread, currentKey, keyDict)
                currentKey+=1

def playThread(thread, key, keyDict):
    """
    Plays the thread's short category.
    """
    debugPrint("PLAYING THREAD #%s, KEY %s", (str(thread),str(key))
    playFile('press-'+str(key)+'-for',keyDict)
    playFile(str(thread)+"/"+'thread-'+str(thread),keyDict)

def walkCategoryTree(intro, outro, parent, keyDict):
    """
    Walks the category tree and returns id of the category selected.
    Parent may be None for the main menu.
    Intro may be None (outro should not be)
    """
    debugPrint("walk category tree def") 
    parentKeyDict = keyDict
    keyDict = dict(keyDict) # deep copy
    children = db.getCategoryChildren(parent)
    #Return if we're the deepest node
    if len(children)==0:
        return parent
    
    accessibleChildren = children[:7]

    for i in xrange(len(accessibleChildren)):
        keyDict[str(3+i)] = Nop

    categoryKeys = [str(i) for i in xrange(3,len(accessibleChildren)+3)]
    #FIXME: we may eventually want to play an additional file to say '0'
    # brings you up a menu level; currently, main-menu-intro includes this
    #refactor me... :(

    try:
        while True:
            #Play intro
            if intro:
                res = playFile(intro,keyDict)
                if res in categoryKeys:
                    x = walkCategoryTree(intro,
                                         outro,
                                         accessibleChildren[int(res)-3],
                                         parentKeyDict)
                    if x == '0':
                        continue
                    else:
                        return x
            
            #Play children nodes
            res = None
            for child, key in zip(accessibleChildren,
                                  range(3,len(accessibleChildren)+3)):
                res = playCategory(child, key, keyDict)
                if res in categoryKeys:
                    break
            #If we received a relevant keypress, recurse
            if res in categoryKeys:
                x = walkCategoryTree(intro,
                                     outro,
                                     accessibleChildren[int(res)-3],
                                     parentKeyDict)
                if x == '0':
                    continue
                else:
                    return x
            #Play outro
            res = playFileGetKey(outro, 10, 1, keyDict)
            if res in categoryKeys:
                x =  walkCategoryTree(intro,
                                      outro,
                                      accessibleChildren[int(res)-3],
                                      parentKeyDict)
                if x == '0':
                    continue
                else:
                    return x        
    except KeyPressException, e:
        if e.key == '0':
            #go up a level
            return '0'
        else:
            raise

def playCategory(category, key, keyDict):
    debugPrint("play category definition") 
    res = playFile('press-'+str(key)+'-for',keyDict)
    if res in keyDict:
        return res
    playFile('category-'+str(category),keyDict)
    if res in keyDict:
        return res
    return ''
    
def readThread(thread):
    """
    Implements the read thread state.
    """
    debugPrint("READING COMMENTS IN THREAD")
    keyDict = newKeyDict()
    keyDict['1'] = (addComment,(thread,))

    playFile('comment-intro',keyDict)
    playFile(str(thread)+'/'+'thread-'+str(thread),keyDict)
    newComments = db.recentCommentLookup(user,thread)
    for comment in newComments:
        keyDict['2'] = (skipComment, (comment,))
        commentListen(thread,comment,keyDict)
        db.updateUserCommentLocation(user,thread,comment)
        debugPrint("THREAD: %s, COMMENT: %s", (thread, comment))
    allComments = db.allCommentLookup(thread)
    for comment in allComments:
        commentListen(thread,comment,keyDict)
    RaiseZero()

def commentListen(thread,comment,keyDict):
    return playFile(str(thread)+'/'+str(comment),keyDict)

def addComment(thread):
    while True:
        fname = recordFilePlayback('add-comment',60.0)
        if fname:
            break
    commentNum = db.addComment(thread,user)
    #BUG UNHANDLED RACE CONDITION (added to db before the file's moved)
    os.rename(SOUND_DIR+fname+'.wav',SOUND_DIR+str(thread)+'/'+str(commentNum)+'.wav')
    readThread(thread)

def recordUserMessage():
    while True:
        fname = recordFilePlayback('record-greeting-request',10.0)
        if fname:
            break
    os.rename(SOUND_DIR+fname+'.wav',SOUND_DIR+'user-'+user+'.wav')
    db.addUser(user)
    

def recordFilePlayback(introFilename, recordLen):
    """
    Plays the specified intro file. Records a file of specified length (in
    ms)
    Returns the filename created, or none if the file was deleted.
    Throws a keypress exception if an unrecognized key is pressed (e.g. 0)
    """
    keyDict = newKeyDict()
    try:
        playFile(introFilename,keyDict)
        name = os.tmpnam()
        name = name[len('/tmp/'):]
        recordFile(name, '#01', recordLen , 5)
        #Add options
        playFile(name,keyDict)
        while True:
            keyDict['1']= Nop
            keyDict['2']= (removeTempFile,(SOUND_DIR+name+'.wav',))
            key = playFileGetKey('keep-or-rerecord',5000,1,keyDict)
            if key == '1':
                return name
            elif key == '2':
                return None
            else:
                playFile('not-understood')

    except KeyPressException, e:
        if name and os.path.exists(SOUND_DIR+name+'.wav'):
            os.remove(SOUND_DIR+name+'.wav')
        raise

def personalOptions():
    keyDict = newKeyDict()
    keyDict['1'] = addTopic
    keyDict['2'] = addFriend
#   keyDict['3'] = recentPosts
#   keyDict['4'] = broadCast
#   keyDict['5'] = changeVoiceName
    while True:
        playFile('personal-options-intro', keyDict)

def addTopic():
    blankDict = newKeyDict()
    chooseCategoryDict = newKeyDict()
    subjName = recordFilePlayback('record-subject',20)
    debugPrint(subjName)
    commentName = recordFilePlayback('record-comment',60)
    parentID = walkCategoryTree('choose-category','confirmation-sound', None, chooseCategoryDict)
    db.addComment(parentID, user)
    id = db.addThread(parentID, user) #should return ID
    os.mkdir(SOUND_DIR+str(id)) #makes directory 
    os.rename(SOUND_DIR+subjName+".wav", SOUND_DIR+str(id)+"/"+"thread-"+str(id)+".wav")
    os.rename(SOUND_DIR+commentName+".wav", SOUND_DIR+str(id)+"/"+"comment-"+str(id)+".wav")
    playFile('thanks-for-posting', blankDict)
    #os.remove(SOUND_DIR+commentName+".wav")
    #os.remove(SOUND_DIR+subjName+".wav")
    personalOptions()
	
def addFriend():
    blankDict = {}
    keyDict = newKeyDict()
    number = 0
    number = playFileGetKey('enter-friend-number', 10, 11, blankDict)
    keyDict['1'] = (addFriendConfirm,(number,))
    keyDict['2'] = addFriend
    #'Please enter your friend's phone number'
    sayNumber(number)
    while True:
        playFile('confirm-or-retry', keyDict)

def addFriendConfirm(number):
    db.addFriend(number, user) #user must be users number
    playFile('friend-added-thanks',newKeyDict())
    personalOptions()

 
### Procedural code starts here ###
if __name__=='__main__':
    if DEBUG:
        db = Database(db_name='test',db_port=3306)
        user = '123456'
    else:
            # Read and ignore AGI environment (read until blank line)
        env = {}
        tests = 0;
        while True:
            line = sys.stdin.readline().strip()
            if line == '':
                break
            key,data = line.split(':')
            if key[:4] != 'agi_':
                #skip input that doesn't begin with agi_
                sys.stderr.write("Did not work!\n")
                sys.stderr.flush()
                continue
            key = key.strip()
            data = data.strip()
            if key != '':
                env[key] = data
        sys.stderr.write("AGI Environment Dump:\n")
        sys.stderr.flush()
        for key in env.keys():
            sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
            sys.stderr.flush()
        db = Database()
        user = env['agi_calleridname']
    login()
    while True:
        try:
            mainMenu()
        except KeyPressException, e:
            if e.key != '0':
                raise
            else:
                continue
