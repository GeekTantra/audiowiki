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
    from database import *

SOUND_DIR = '/var/lib/asterisk/sounds/audiowiki-beta' # New Sound Directory
AST_SOUND_DIR = '/var/lib/asterisk/sounds' # New Sound Directory
LANGUAGE = 'noLanguageSet'

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

def setLanguage(language):
    global LANGUAGE
    debugPrint(LANGUAGE)
    LANGUAGE = language
    debugPrint(LANGUAGE)
    mainMenu()
    
def mainMenu():
    """
    Main Menu: All the available categories are played for the user, and he is free to
    select what interests him. The moderator says "Press 1 for " and then the category
    sound file is played. This system supports anywhere from 1 to 9 categories. Selecting
    a category sends the user to a list of user-generated comments.
    
    Audio Files:
    mainMenu-intro -- " "
    mainMenu-outro -- "To hear these options again, please stay on the line. To 
                       explore other options, press *."
    star-for-moreInfo -- "Press * for more information about this system."
    login-for-pfVersion -- "Welcome to Audio Wikipedia. To jump to a specific forum, please
                            enter the forum key followed by pound. To browse public forums,
                            press pound now, or wait on the line."    

    NOTE: star-for-moreInfo is an optional message. Feel free to comment out
    as necessary. See instructions below.
    """

    global LANGUAGE
    debugPrint('LANGUAGE = ' + LANGUAGE)
    languageKeyDict = newKeyDict()
    languages = db.getLanguages()   # get list of all languages from database
    debugPrint(str(languages))
    for i in range(len(languages)): # when a language is selected,
                                    # call the function by its name
                                    # here, we set the function to the keypress
	languageKeyDict[str(i+1)] = (setLanguage, (languages[i],))
    if LANGUAGE == 'noLanguageSet':
        while True:
            for language in languages:
                playFile(SOUND_DIR+'/public_sounds/press-'+str(languages.index(language)+1)+'-for',\
                                                                         languageKeyDict)
                playFile(SOUND_DIR+'/global/'+language+'/'+language,languageKeyDict)
                playFile(SOUND_DIR+'/public_sounds/shortSilence',languageKeyDict)
            playFile(SOUND_DIR+'/public_sounds/longSilence',languageKeyDict)

    # goToPrivateForum()

    # debugPrint("IN MAIN MENU, THE LANGUAGE IS " + language)

    keyDict = newKeyDict()
    #keyDict['*'] = (RaiseKey,('*',))

    #playFile('star-for-moreOptions', keyDict)

    try:
        while True:
            categoryKey = playCategoryMenu(None, 'mainMenu-outro', keyDict)
            # w/o intro
          # categoryKey = playCategoryMenu('mainMenu-intro','mainMenu-Outro', keyDict)
            # w/ intro
            if categoryKey != '0':
                break
    except KeyPressException, e:
        if e.key == '*':  
            moreOptions()  #THIS METHOD HAS NOT YET BEEN IMPLEMENTED
            return          
        else:               
            raise
    playCommentsInCategory(categoryKey, None)
    
def goToPrivateForum():
    """
    """
    goToPrivForum = playFileGetKey('mainMenuIntro',6,20,{})
    if goToPrivForum:
        privateForumIntroFileName = db.getPrivateForumIntroFileName(goToPrivForum)
        if privateForumIntroFileName:
            playCommentsInCategory(goToPrivForum, privateForumIntroFileName)
        else:
            playFile('not-understood')
            goToPrivateForum()

def playCategoryMenu(introAudio, outroAudio, keyDict):
    """
    This part of the main menu plays the available category options for the user.
    While listening to these options, he can listen to the comments in the category
    by pressing the designated key for that category. This method plays the options
    and returns the user's keypress.
    
    The intro file plays before the category options and the outro, plays afterward.
    If you don't want an intro, supply the argument None. An outro is required to let
    the user know that he has listened to all the available options.

    Audio Files:
    under-construction -- "We're sorry but this system is currently under construction.
                           Please check back later! Thank You."
    listening-to-comments -- "While listening to comments, press 1 to add a comment,
                                or, press 2 to skip to the next one.
    """
    categoryKeys = db.getKeys() # Gets the keys corresponding to all the
                                # available categories in the system from
                                # the database.
    debugPrint(str(categoryKeys))
    if not categoryKeys:
        debugPrint("NO CATEGORIES IN DATABASE")
        while(True):
            playFile('under-construction', keyDict)
            playFile('wait-10')
    debugPrint(str(categoryKeys))
    for key in categoryKeys:
        keyDict[str(key)] = (playCommentsInCategory, (key, 'listening-to-comments',))
    while True:  # Menu = Intro + Category Options + Outro
                 # Loop through this menu endlessly.
        if introAudio:
            userInput = playFile(introAudio, keyDict)
            if userInput in categoryKeys:
                return userInput
        userInput = None
        for key in categoryKeys:
            userInput = playCategoryTitle(key, keyDict) # Remember, key corresponds
                                                        # to category and dialpad
            if userInput in categoryKeys:
                return userInput
        userInput = None
        userInput = playFile(outroAudio, keyDict)
        userInput = playFile('breathing-13-seconds',keyDict)
        if userInput in categoryKeys:
            return userInput

def playCategoryTitle(categoryKey, keyDict): # We refer to the 'title' file as the sound file
                                             # created by the administrator that describes
                                             # the topic of that category.
    """
    Audio Files:
    category-1-title -- a category title
    category-2-title
        .
        .
        .
    category-9-title
    """
    titlePath = SOUND_DIR + "/global/" + LANGUAGE + "/" + str(categoryKey) \
                                + "/" + str(categoryKey) + "-title"
    # numAudio = SOUND_DIR + "/" + LANGUAGE + "/narratedDigitOptions/press-" \
    #                           + str(categoryKey) + "-for"
    # playFile(numAudio,keyDict)
    return  playFile(titlePath, keyDict)

def playCommentsInCategory(categoryKey, commentIntroAudio):
    """
    This method plays all the comments in a given categoroy. The order can be changed
    by an Administrator. He can choose from the following options:
        - most recent first
        - most recent a user has heard
            NOTE: This requires that the user has Caller-ID, which is used to
                  uniquely identify callers.
        - most listened to first
        - shuffle (random) order

    Audio Files:
    empty-category -- "There aren't any comments in this category. Press 1 to add a comment.
                       or press 0 to go back to the main menu."
    end-of-comments -- "You have just heard all the comments in this category, to return to the
                        main menu, please press 0. To add a comment press 1. To listen to the
                        comments again, please stay on the line."
    """
    debugPrint(str(categoryKey))
    commentList = db.getCommentList(user, categoryKey, LANGUAGE)
    
    keyDict = newKeyDict()
    keyDict['1'] = (addComment,(categoryKey,))
#   keyDict['2'] = (jumpToComment,(categoryKey,))
#   keyDict['3'] = (shuffleComments(),('3',)) # Hidden, the moderator does not
                                              # voice this option.
                                              
    debugString = "PLAYING CATEGORY " + str(categoryKey) + " FOR USER " + str(user)

    if commentIntroAudio and len(commentList) != 0:
        userInputDuringIntro = playFile(commentIntroAudio, keyDict)
    if len(commentList) == 0:
        playFile('empty-category', keyDict)
        return
    for commentID in commentList:
        keyDict['#'] = (skipComment,(commentID,))
        debugPrint("CATEGORY: "+str(categoryKey)+" COMMENT: "+str(commentID)+" BEING PLAYED")
        playComment(commentID, categoryKey, keyDict)
        #userInput = str(playComment(commentID, categoryKey, keyDict))
        #if userInput == '0': # If user listens to comment w/o skipping, subtract one \
                             # from skip_count
        #    db.hasPlayed(commentID)
        #db.updateUserCursor(user, categoryKey, commentID)
    # All comments are finished playing, alert the user to either wait, press 0 or listen
    # to the comments again.
    FinishedPlayingMsg = "FINISHED PLAYING ALL COMMENTS IN CATEGORY " + str(categoryKey) \
    + ", PRESS 0 TO RETURN TO MAIN MENU, 1 TO ADD A COMMENT OR NOTHING TO LISTEN AGAIN."
    debugPrint(FinishedPlayingMsg)
    playFile('end-of-comments', keyDict)
    playFile('breathing-13-seconds',keyDict)
    playCommentsInCategory(categoryKey, commentIntroAudio)
    RaiseZero()

def jumpToComment(categoryKey):
    jumpToThisCommentID = playFileGetKey('enter-commentID',6,5,{})
    jumpingMessage = "JUMPING TO COMMENT " + jumpToThisCommentID
    debugPrint(jumpingMessage)
    db.updateUserCursor(user, categoryKey, jumpToThisCommentID)
    InCategory(categoryKey, None)

def skipComment(commentID):
    db.skipComment(int(commentID))
    
def playComment(commentID, categoryKey, keyDict):
    """
    Plays the comment with id, commentID in category, categoryKey.    
    """
    debugString = "PLAYING COMMENT " + str(commentID) + " IN CATEGORY " + str(key)
    debugPrint(debugString)
    return playFile("audiowiki-beta/global/" + LANGUAGE + "/" + str(categoryKey) \
                    + "/" + str(commentID), keyDict)

def addComment(categoryKey):
    """
    Allows the user to add a comment. This method first asks the user to record a comment,
    using the recordFilePlayback method. Then, once the file has been recorded, it adds the
    comment data (time added and commenter) to the database.
    
    Audio Files:
    add-comment -- "Start your comment after the tone. When you're done, press #."
    comment-added -- "Thank you. Your comment has been added."
    """
    while True:
        commentTempFileName = recordFilePlayback("add-comment",300)
        if commentTempFileName:
            break
    newCommentID = db.addComment(categoryKey, user,LANGUAGE)
    # if not os.path.lexists(SOUND_DIR+"/"+str(categoryKey)):
    #    os.mkdir(SOUND_DIR + "/" + str(categoryKey))
    if not os.path.lexists(SOUND_DIR+"/global/"+LANGUAGE+"/"+str(categoryKey)+"/web"):
         os.mkdir(SOUND_DIR+"/global/"+LANGUAGE+"/"+str(categoryKey)+"/web")
         os.chmod(SOUND_DIR+"/global/"+LANGUAGE+"/"+str(categoryKey)+"/web",0777)
    os.rename(AST_SOUND_DIR+"/"+commentTempFileName+".wav",SOUND_DIR+"/global/"+LANGUAGE+"/"+\
                              str(categoryKey)+"/"+str(newCommentID)+".wav")
    os.system("lame -h --abr 200 " + SOUND_DIR + "/global/"+LANGUAGE+"/" \
                              + str(categoryKey) +"/"+str(newCommentID) + ".wav " + \
              SOUND_DIR + "/global/" + LANGUAGE+"/"+ str(categoryKey) + "/web/" + str(newCommentID) \
                              + ".mp3")
    playFile('comment-added')
    playCommentsInCategory(categoryKey, None)

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
        playFile(introFilename,keyDict)
        recordFile(name, '#01', recordLen, 5)
        # Add options
        playFile(name, keyDict)
        while True:
            keyDict['1']= Nop
            keyDict['2']= (removeTempFile,(AST_SOUND_DIR+"/"+name+'.wav',))
            key = playFileGetKey('submit-or-rerecord', 5000, 1, keyDict)
            if key == '1':
                return name
            elif key == '2':
                return None
            else:
                playFile('not-understood')

    except KeyPressException, e:
        if name and os.path.exists(AST_SOUND_DIR+name+'.wav'):
            debugPrint("STOPS WORKING HERE") # Could be a permissions issue with os.remove?
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
