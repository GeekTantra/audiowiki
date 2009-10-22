#interface to asterisk. Safe for import * ing.
from utilities import *
import re

def checkresult (params):
    """
    Reads the asterisk response and returns the parse result
    """
    params = params.rstrip()
    if re.search('^200',params):
        result = re.search('result=([\d*#]+)',params)
        if (not result):
            sys.stderr.write("FAIL ('%s')\n" % params)
            sys.stderr.flush()
            return -1
        else:
            result = result.group(1)
            #debug("Result:%s Params:%s" % (result, params))
            sys.stderr.write("PASS (%s)\n" % result)
            sys.stderr.flush()
            return result
    else:
        sys.stderr.write("FAIL (unexpected result '%s')\n" % params)
        sys.stderr.flush()
        return -2

def playFile (fname, keyDict = newKeyDict()):
    """
    Plays the file "fname". keyDict is a dictionary mapping characters from
    the number pad to functions of zero arguments which are called in the
    case of a keypress, or tuples of functions and their arguments
    """
    escapeDigits = ''
    for key in keyDict:
        escapeDigits += key
    debugPrint("STREAM FILE %s \"%s\"\n" % (str(fname),escapeDigits))
    sys.stdout.write("STREAM FILE %s \"%s\"\n" % (str(fname),escapeDigits))
    sys.stdout.flush()
    result = sys.stdin.readline().strip()      
    result = checkresult(result)
    if (not isinstance(result,str)) or result == '-1':
        return -1
    elif result == '0':
        return 0
    else:
        #if the user pressed a key...
        c = chr(int(result))
        if isinstance(keyDict[c],tuple):
            keyDict[c][0](*keyDict[c][1])
        else:
            keyDict[c]()
        return c

def recordFile (fname, stopDigits, timeout, silenceTimeout):
    """
    Records a file to the local disk.
    fname is the name of the file to record (minus .wav)
    stopDigits are keys that stop recording (not returned)
    timeout is the total time allowed for the recording in seconds
    silenceTimout is the silence time before the recording ends
    automatically in seconds
    """
    ms_timeout = -1 #int(timeout*1000)
    seconds_silenceTimeout = -1 #int(silenceTimeout)
    cmdString = "RECORD FILE %s wav %s %s BEEP s=%d\n" % (fname, \
                                                          stopDigits, \
                                                          ms_timeout, \
                                                          seconds_silenceTimeout)
    debugPrint(cmdString)
    sys.stdout.write(cmdString)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    result = checkresult(result)
    return result

def playFileGetKey (prompt, timelimit, digcount, keyDict):
    """
    Plays a file to the user and waits for up to digcount keypresses during
    seconds.
    """
    timelimit = int(timelimit*1000);
    
    sys.stderr.write("GET DATA %s %d %d\n" % (prompt, timelimit, digcount))
    sys.stderr.flush()
    sys.stdout.write("GET DATA %s %d %d\n" % (prompt, timelimit, digcount))
    sys.stdout.flush()
    
    result = sys.stdin.readline().strip()
    result = checkresult(result)

    sys.stderr.write("digits are %s\n" % result)
    sys.stderr.flush()

    if isinstance(result,str):
        if result in keyDict:
            if isinstance(keyDict[result],tuple):
                keyDict[result][0](*keyDict[result][1])
            else:
                keyDict[result]()
        return result
    else:
        return ''

def sayNumber(number):
    """
    Says number aloud to user.
    """
    sys.stderr.write("SAY NUMBER %s \"\"\n" % str(number)) 
    sys.stderr.flush()
    sys.stdout.write("SAY NUMBER %s \"\"\n" % str(number)) 
    sys.stdout.flush() 
    result = sys.stdin.readline().strip() 
    