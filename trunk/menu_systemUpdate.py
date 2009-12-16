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
        print 'Usage: ' + sys.argv[0] + ' [auto|man]'
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
    from databaseUpdate import *

SOUND_DIR = '/var/lib/asterisk/sounds/audiowikiIndia/'
AST_SOUND_DIR = '/var/lib/asterisk/sounds/'

sys.setrecursionlimit(15000)

##### State functions ######

def login():
    """
    Login: If the user's phone number (var 'user') is unrecognized,
    the system stores it in the "user" table.

    Audio Files:
    """
    if not db.isUser(user): # If the phone number calling the system is
                            # unrecognized by the database, add the number
                            # as a new user to table 'users'.
        db.addUser(user)
        newUserMessage = str(user) + " ADDED TO DATABASE"
        debugPrint(newUserMessage) # Print message to Asterisk console. NOTE: You must run
                                   # the agi-debug command at console before debug messages
                                   # will appear.
    elif db.isUser(user):
        returningUserMessage = "RETURNING USER " + str(user)
        debugPrint(returningUserMessage)
    
def mainMenu():
    """

    """
    keyDict = newKeyDict()
#    keyDict['*'] = (RaiseKey,('*',))

    #playFile('star-for-moreOptions', keyDict)

    playFile(SOUND_DIR+'welcome-message',keyDict)
    """
    Welcome to Audio Wiki!
    """

    try:
        while True:
            playStream()           
    except KeyPressException, e:
        if e.key == '*':  
            debugPrint("Here")
            addComment()
            return          
        else:               
            raise

def playStream():
    keyDict = newKeyDict()
    keyDict['*'] = (addComment,())
    commentIDs = db.getCommentIDs()
    if len(commentIDs) == 0:
        return playFile(SOUND_DIR+'no-comments',keyDict)
    playFile(SOUND_DIR+'instructions',keyDict)
    """
    This is a user generated audio stream. To skip to the next post, press 2.
    """
    for commentID in commentIDs:
        keyDict['1'] = (skipComment,(commentID,))
        commentFile = SOUND_DIR+str(commentID)
        keyPress = playFile(commentFile, keyDict)
        if keyPress == '1': # If user presses 1, skip to next comment.
            pass
    playFile(SOUND_DIR+'stream-over', keyDict)
    """
    You've just heard all the comments on this stream. To hear it again, please
    wait on the line.
    """

def skipComment(commentID):
    debugPrint("SKIPPING COMMENT "+str(commentID))
    db.skipComment(int(commentID))

def addComment():
    """
    
    """
    while True:
        commentTempFileName = recordFilePlayback("add-comment",300)
        """
        Record your comment after the tone. Press 1 when you're done.
        """
        if commentTempFileName:
            break
    newCommentID = db.addComment(user)
    os.rename(AST_SOUND_DIR+commentTempFileName+".wav", SOUND_DIR+str(newCommentID)+".wav")
    os.system("lame -h --abr 200 "+SOUND_DIR+str(newCommentID)+".wav "+SOUND_DIR+"/web/" \
                                                              + str(newCommentID)+".mp3")
    playFile(SOUND_DIR+'comment-added')
    """
    Your comment is now available on this stream! Thanks for posting!
    """
    playStream()
    
def recordFilePlayback(introFilename, recordLen):
    """
    Plays the specified intro file. Records a file of specified length (in
    ms)
    Returns the filename created, or none if the file was deleted.
    Throws a keypress exception if an unrecognized key is pressed (e.g. 0)

    Audio Files:
    keep-or-rerecord -- "Press 1 to submit this comment or press 2 to re-record."
    not-understood -- "Sorry, but I didn't understand that command."
    """
    keyDict = newKeyDict()
    name = os.tmpnam()
    name = name[len('/tmp/'):]
    try:
        playFile(SOUND_DIR+introFilename,keyDict)
        recordFile(name, '#01', recordLen, 5)
        # Add options
        playFile(name, keyDict)
        while True:
            keyDict['1']= Nop
            keyDict['2']= (removeTempFile,(AST_SOUND_DIR+"/"+name+'.wav',))
            key = playFileGetKey(SOUND_DIR+'submit-or-rerecord', 5000, 1, keyDict)
            """
            Press 1 to submit this comment, or press 2 to re-record.
            """
            if key == '1':
                return name
            elif key == '2':
                return None
            else:
                playFile(SOUND_FILE+'not-understood')
                """
                I didn't catch that.
                """

    except KeyPressException, e:
        if name and os.path.exists(AST_SOUND_DIR+name+'.wav'):
            os.remove(AST_SOUND_DIR+name+'.wav')
        raise

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
