#DB Functions

#import * safe
import MySQLdb
import re
from utilities import *

DB_USER = 'python'
DB_PASSWD = 'rock+bait'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'audiowikiIndia'

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
            "SELECT phone_number FROM users WHERE phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def getCommentIDs(self):
        self.c.execute("""SELECT id from comments WHERE archived = 0 \
                        ORDER BY time DESC;""")
        # Select the comments that haven't been archived.
        comments = self.c.fetchall()
        comments = [i[0] for i in comments]
        return comments
           
    def addComment(self,phoneNum):
        self.c.execute("INSERT INTO comments (user) VALUES (%s);", \
                       (phoneNum))
        self.db.commit()
        return self.c.lastrowid

    def skipComment(self, commentID):
        self.c.execute(
            "UPDATE comments SET skip_count = skip_count + 1 WHERE id = %s;",
            (commentID))
        self.db.commit()
        debugPrint("SKIPPED "+str(commentID))
