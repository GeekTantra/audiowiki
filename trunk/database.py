#DB Functions

#import * safe
import MySQLdb
import re
from utilities import *

DB_USER = 'python'
DB_PASSWD = 'rock+bait'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'audiowikibeta'

class Database:
    def __init__(self,db_port=DB_PORT,db_host=DB_HOST,
                db_user=DB_USER,db_passwd=DB_PASSWD,db_name=DB_NAME):
        self.db = MySQLdb.connect(port=db_port,host=db_host,
                                user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')

    def addUser(self, phoneNumberString):
        self.c.execute("INSERT INTO users (phone_number) " + \
                       "VALUES (%s);",(str(phoneNumberString),))
        self.db.commit()

    def isUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM users WHERE phone_number = %s;",(str(phoneNumberString),))
        return count>0

    def getKeys(self):
        self.c.execute("""SELECT `key` FROM categories;""")
        results = self.c.fetchall()
        keys = [i[0] for i in results]
        return keys
   
    def getCommentList(self, phoneNumberString, categoryKey):        
        usersCursors = self.getCursor(phoneNumberString)
        if str(categoryKey) in usersCursors and phoneNumberString != 'Unavailable':
                                                # If the user has listened to comments in
                                                # this category before and has caller id,
                                                # retrieve the comment list starting from                                                 # comment not listened to and ending with
                                                # most recent to the least recent (oldest)
                                                # comment.
            self.c.execute(
                "SELECT id FROM comments WHERE `key` = %s AND id > %s "+\
                "ORDER BY time ASC;",
                           (str(categoryKey), usersCursors[str(categoryKey)]))
        else: # If the user has not listened to comments in this category before,
              # retrieve the comment list starting from the most recent comment
              # and ending with the least recent (oldest) comment.
            self.c.execute("""SELECT id FROM comments
                           WHERE `key` = %s ORDER BY time ASC;""",
                           (str(categoryKey),))
        results = self.c.fetchall()
        commentList = [i[0] for i in results]
        debugPrint(str(commentList))
        if commentList == []:
            self.c.execute("""SELECT id FROM comments
                           WHERE `key` = %s ORDER BY time ASC;""",
                           (str(categoryKey),))
            results = self.c.fetchall()
            commentList = [i[0] for i in results]
            debugPrint("YOU'VE LISTENED TO ALL THE COMMENTS, PLAYING FROM START")
            debugPrint(str(commentList))
        return commentList

    def getAllComments(self, categoryKey):
        self.c.execute("""SELECT id FROM comments WHERE `key` = %s ORDER BY time ASC;""", \
                       (str(categoryKey),))
        results = self.c.fetchall()
        allComments = [i[0] for i in results]
        return allComments

    def getCursor(self, phoneNumberString):
        count = self.c.execute(
            "SELECT thread_cursor FROM users WHERE phone_number = %s;",
            (phoneNumberString,))
        assert(count == 1L) # If the assertion is true, the program continues
                            # Otherwise, the program stops and brings up an
                            # AssertionError with this line.
        cursor = _parseCursor(self.c.fetchall()[0][0])
        return cursor

    def updateUserCursor(self, phoneNumberString, categoryKey, commentID):
        userLocation = self.getCursor(phoneNumberString)
        userLocation[str(categoryKey)] = str(commentID)
        formattedString = _formatCursor(userLocation)
        self.c.execute(
            "UPDATE users SET thread_cursor = %s WHERE phone_number = %s;",
            (formattedString, phoneNumberString))
        self.db.commit()

    def hasPlayed(self, commentID):
        self.c.execute("""UPDATE comments SET skip_count = skip_count - 1
                            WHERE id = %s;""", (int(commentID),))
        debugPrint(str(commentID) + " HAS FINISHED PLAYING")

    def addComment(self,categoryKey,phoneNum):
        self.c.execute("INSERT INTO comments (`key`, commenter) VALUES (%s,%s);", \
                       (categoryKey,phoneNum))
        self.db.commit()
        return self.c.lastrowid

    def skipComment(self, commentID):
        self.c.execute(
            "UPDATE comments SET skip_count = skip_count + 1 WHERE id = %s;",
            (commentID))
        self.db.commit()
        self.c.execute(
            "SELECT `key` FROM comments WHERE id = '%s';",
            (commentID))
        results = self.c.fetchall()
        key = [i[0] for i in results]
        debugPrint("SKIPPED " + str(commentID) + ", IN CATEGORY, " + str(key))

    def getPrivateForumIntroFileName(self, forumKey):
        self.c.execute(
            "SELECT introFileName FROM privateForums WHERE forumKey = %s;",
            (forumKey))
        self.db.commit()
        results = self.c.fetchall()
        if results:
            debugPrint(str(results))
            introFileName = [i[0] for i in results][0]
            return introFileName
        else:
            return ""

def _parseCursor(string):
    """
    Parses a string in the format ((\w+):(\w+),)* into a dict where the
    key is to the left of the ':' and the value is between the ':' and the ','

    Note that if string is not a string, this returns an empty dictionary.
    
    Inverse function is formatThreadCursor
    """
    if (not string) or (not isinstance(string,str)):
        return {}
    groups = re.findall('(\w+):(\w+),',string)
    return dict(groups)

def _formatCursor(parsedDict):
    """
    Converts a dictionary into the string format:
    [key]:[value],
    appended to one another.

    Note that key and value must be strictly alphanumeric strings;
    raises a value error if this condition isn't met.
    
    Inverse function is parseThreadCursor.
    """
    res = ''
    for key in parsedDict:
        if (not key.isalnum() or not parsedDict[key].isalnum):
            raise ValueError('Key or value contained non alphanumerics')
        res += key + ':' + parsedDict[key] + ','
    return res
