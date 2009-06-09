#wrapper for database functions
#import * safe
import MySQLdb
import re

DB_USER = 'python'
DB_PASSWD = 'rock+bait'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'test'

#### db wrapper
class Database:
    def __init__(self,db_port=DB_PORT,db_host=DB_HOST,
                db_user=DB_USER,db_passwd=DB_PASSWD,db_name=DB_NAME):
        self.db = MySQLdb.connect(port=db_port,host=db_host,
                                user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')

    def getRecentThreads(self,level,optionsPerLevel):
        self.c.execute("""SELECT id FROM threads order by time;""")
        results = self.c.fetchall()
        #Unpack the tuples
        results = [r[0] for r in results]
        if len(results) < (level+1)*optionsPerLevel:
            return results[-optionsPerLevel:]
        else:
            return results[level*optionsPerLevel:(level+1)*optionsPerLevel]

    def getCategoryChildren(self, parent):
        """
        Gets the child category of the specified parent category.
        If the parent is None, gets the parentless nodes (should be the
        main menu's nodes).
        """
        if not parent:
            self.c.execute("SELECT id FROM categories WHERE parentid IS NULL;")
        else:
            self.c.execute("SELECT id FROM categories WHERE parentid = %s;",
                           (int(parent),))
        children = self.c.fetchall()
        children = [child[0] for child in children]
        return children

    def getCategoryThreads(self, category):
        """
        Gets the threads which are chidren to the specified category.
        """
        self.c.execute(
            "SELECT id FROM threads WHERE categoryid = %s ORDER BY id;",
            (category,))
	threadList = self.c.fetchall()
        threadList = [x[0] for x in threadList] #Get ID value for each thread in selection
        return threadList

    def isUser(self,userString):
        count = self.c.execute(
            "SELECT phoneNum FROM users WHERE phoneNum = %s;",(str(userString),))
        return count>0
    
    def addContactedUser(self, userString):
        self.c.execute("INSERT INTO users (phoneNum, friends, contacted) "+\
                       "VALUES (%s, '', true);",(str(userString),))
        self.db.commit()

    def addUncontactedUser(self, userString):
        self.c.execute("INSERT INTO users (phoneNum, friends, contacted) "+\
            "VALUES (%s, '', false);",(str(userString),))
        self.db.commit()
	return self.c.lastrowid

    def addComment(self,thread,phoneNum):
        self.c.execute(
            "INSERT INTO comments (threadId, phoneNum) VALUES (%s,%s);",
            (thread,phoneNum))
        self.db.commit()
	return self.c.lastrowid

    def addThread(self, categoryid, phoneNum):
        self.c.execute(
            "INSERT INTO threads (categoryid, user) VALUES (%s,%s);",
            (categoryid, phoneNum))
        self.db.commit()
	return self.c.lastrowid

    def isSkipped(self, commentID):
        self.c.execute(
            "UPDATE comments SET skipCount = skipCount + 1 WHERE id = %s;",
            (commentID))
        self.db.commit()
        return self.c.lastrowid

    def getCommentDict(self, userString):
        count = self.c.execute(
            "SELECT threadCursor FROM users WHERE phoneNum = %s;",
            (userString,))
        assert(count==1L)
        commentDict = _parseThreadCursor(self.c.fetchall()[0][0])
        return commentDict

    def updateUserCommentLocation(self, userString, thread, comment):
        userCommentLocation = self.getCommentDict(userString)
        userCommentLocation[str(thread)] = str(comment)
        formattedString = _formatThreadCursor(userCommentLocation)
        self.c.execute(
            "UPDATE users SET threadCursor = %s WHERE phoneNum = %s;",
            (formattedString,userString))
        self.db.commit()

    def recentCommentLookup(self, userString, thread):
        commentDict = self.getCommentDict(userString)
        if str(thread) in commentDict:
            self.c.execute(
                "SELECT id FROM comments WHERE threadId = %s AND id > %s "+\
                "ORDER BY time ASC;",
                           (str(thread),commentDict[str(thread)]))
        else:
            self.c.execute("""SELECT id FROM comments
                           WHERE threadId = %s ORDER BY time ASC;""",
                           (str(thread),))
        res = self.c.fetchall()
        res = [r[0] for r in res]
        return res

    def allCommentLookup(self, thread):
        self.c.execute("""SELECT id FROM comments
                           WHERE threadId = %s ORDER BY time ASC;""",
                           (str(thread),))
        res = self.c.fetchall()
        res = [r[0] for r in res]
        return res

    def addFriend(self, friendNum, friender):
        """
        input: number to add to friends,
	user for whom it will be added

	adds friendnum as a user if not already in the system
	"""
        #BUG: not threadsafe to multiple users calling from same phonenum
	rowCount = self.c.execute("""SELECT friends FROM users WHERE phoneNum = %s;""", (friender,))
	assert(rowCount == 1) #if this fails, we are adding friends to a user not in the system
        friendNum = str(friendNum)
        currentFriends = self.c.fetchall()[0][0]
        if not currentFriends == '':
            if friendNum in currentFriends.split(','):
                return
            newFriends = currentFriends + ',' + friendNum
	else:
            newFriends = friendNum
        self.c.execute("""UPDATE users SET friends=%s WHERE phoneNum = %s;""", (newFriends,friender))
        if not self.isUser(friendNum):
            self.addUncontactedUser(friendNum)
        self.db.commit()

def _parseThreadCursor(string):
    """
    Parses a string in the format ((\w+):(\w+),)* into a dict where the
    key is to the left of the ':' and the value is between the ':' and the ','

    Note that if string is not a string, this returns an empty dictionary.
    
    Inverse function is formatThreadCursor
    """
    if (not string) or (isinstance(string,str)):
        return {}
    groups = re.findall('(\w+):(\w+),',string)
    return dict(groups)

def _formatThreadCursor(parsedDict):
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
