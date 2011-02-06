#DB Functions

#import * safe
import MySQLdb
import re
from utilities import *

DB_USER = 'spark'
DB_PASSWD = 'Ath3n@1094'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'audiwikiswara'

class Database:
    def __init__(self,db_port=DB_PORT,db_host=DB_HOST,
                db_user=DB_USER,db_passwd=DB_PASSWD,db_name=DB_NAME):
        self.db = MySQLdb.connect(port=db_port,host=db_host,
                                user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')
        
    def channelExists(self, channelNum):
        count = self.c.execute("SELECT * FROM stations WHERE number = %s",
                                (str(channelNum),))
        return count>0
        
    def getPostsInChannel(self, channelNum):
        self.c.execute("SELECT * FROM lb_postings WHERE station = %s and status = 3 ORDER BY posted DESC;",
                        (str(channelNum),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts

    def publishPost(self, postID):
        self.c.execute("UPDATE lb_postings SET status = 3 WHERE id = %s;",
                        (str(postID),))
        self.db.commit()

    def archivePost(self, postID):
        self.c.execute("UPDATE lb_postings SET status = 2 WHERE id = %s;",
                        (str(postID),))
        self.db.commit()

    def newCall(self, user):
        self.c.execute("INSERT INTO callLog (user) values (%s);",(str(user),))
        self.db.commit()

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
        self.c.execute("""SELECT id from lb_postings WHERE status = 3 \
                        ORDER BY posted DESC;""")
        # Select the comments that haven't been archived.
        comments = self.c.fetchall()
        comments = [i[0] for i in comments]
        return comments

    def getAllCommentIDs(self):
        self.c.execute("""SELECT id from lb_postings ORDER BY posted DESC;""")
        # Select the comments that haven't been archived.
        comments = self.c.fetchall()
        comments = [i[0] for i in comments]
        return comments

   
    def addCommentToChannel(self, phoneNum, channel):
        self.c.execute("INSERT INTO lb_postings (user, station) VALUES (%s, %s);",(phoneNum, str(channel),))
        self.db.commit()
        ids = str(self.c.lastrowid)
        extension = '.mp3'
        filename = ids + extension
        print filename
        self.c.execute("UPDATE lb_postings SET audio_file = %s WHERE id = %s;",(filename, ids)) 
        self.db.commit()
        return ids

    def addComment(self, phoneNum):
        self.c.execute("INSERT INTO lb_postings (user) VALUES (%s);", \
                       (phoneNum))
        self.db.commit()
        return self.c.lastrowid

    def skipComment(self, commentID):
        self.c.execute(
            "UPDATE lb_postings SET skip_count = skip_count + 1 WHERE id = %s;",
            (commentID))
        self.db.commit()
        debugPrint("SKIPPED "+str(commentID))

    def addPlaybackEvent(self, postID, duration):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto) VALUES (%s, %s, %s);",('Listened', str(postID), str(duration),))
        self.db.commit()
        return self.c.lastrowid

    def addSkipEvent(self, postID, duration):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto) VALUES (%s, %s, %s);",('Skipped', str(postID), str(duration),))
        self.db.commit()

    def addInvalidkeyEvent(self, key, when, duration):
        self.c.execute("INSERT INTO analytics (eventype, invdgtpsd, context, whenpressed) VALUES (%s, %s, %s, %s);",('Invalid Keypress', str(key), str(when), str(duration),))
        self.db.commit()

    def addMessageRecordEvent(self, postID):
        self.c.execute("INSERT INTO analytics (eventype, msgrcd) VALUES (%s, %s);",('Recorded', str(postID),))
        self.db.commit()

    def getID(self):
        self.c.execute("""SELECT id FROM cdr ORDER BY calldate DESC LIMIT 1;""")
        callidno = self.c.fetchall()

    def addCellNumSeries(self, series,provider,circle):
        self.c.execute("INSERT INTO mobileseries (series,provider,circle)  VALUES (%s, %s, %s);", (series, provider, circle,))
        self.db.commit()

    def getCircleForSeries(self,series):
        self.c.execute("SELECT circle from mobileseries WHERE series = %s;", (series,))
        # Select the comments that haven't been archived.
        circle = self.c.fetchall()
        circle = [i[0] for i in circle]
        if circle !=[] and circle[0].strip('\n').strip('\r')!='':
            return circle[0].strip('\n').strip('\r')
        else:
            return None

    def getFeaturedPosts(self):
        self.c.execute("""SELECT *  FROM lb_postings WHERE status = '3' AND posted < NOW()  AND ( tags LIKE '%featured%') ORDER BY posted DESC LIMIT 0,1""")
        posts = self.c.fetchall();
        posts = [i[0] for i in posts]
        return posts

    # Arjun's changes for localization
    def addCircleData(self,circle,circlename,language):
        self.c.execute("INSERT INTO circledata (circle, circlename, language) VALUES (%s, %s, %s);",(circle, circlename, language,))
        self.db.commit()

    def getLanguageForCircle(self,circle):
        self.c.execute("SELECT language from circledata WHERE circle = %s;", (circle,))
        # Select the comments that haven't been archived.
        language = self.c.fetchall()
        language = [i[0] for i in language]
        if language !=[] and language[0].strip('\n').strip('\r')!='':
            return language[0].strip('\n').strip('\r')
        else:
            return None

    def getNumCallsByDate(self):
        self.c.execute("SELECT DATE(timeOfCall), count(*) from callLog GROUP BY DATE(timeOfCall) ORDER BY DATE(timeOfCall);")
        # Select the comments that haven't been archived.
        calls = self.c.fetchall()
        #calls = [i[0] for i in calls]
        return calls

    def getNumCallsByCircle(self):
        self.c.execute("select circle,sum(numcalls) from (select count(*) as numcalls,mobileseries.circle as circle,mobileseries.series as series from callLog,mobileseries where (substr(callLog.user,1,4)=mobileseries.series) group by mobileseries.series) as callsbyseries group by circle order by sum(numcalls) desc;")
        # Select the comments that haven't been archived.
        calls = self.c.fetchall()
        #calls = [i[0] for i in calls]
        return calls

    def getNumCallsByProvider(self):
        self.c.execute("select provider,sum(numcalls) from (select count(*) as numcalls,mobileseries.provider as provider,mobileseries.series as series from callLog,mobileseries where (substr(callLog.user,1,4)=mobileseries.series) group by mobileseries.series) as callsbyseries group by provider order by sum(numcalls) desc;")
        # Select the comments that haven't been archived.
        calls = self.c.fetchall()
        #calls = [i[0] for i in calls]
        return calls

    def getPostsForCaller(self,user):
        circle=self.getCircleForSeries(user[:4])
        #print circle
        query= "SELECT id,tags FROM lb_postings WHERE station = 12345 and status = 3 and tags like  '%%NAT%%' or tags like '%%%s%%' or tags like '%%CUL%%' ORDER BY posted DESC;" %circle
        self.c.execute(query)
        #self.c.execute("SELECT id,tags FROM lb_postings WHERE station = 12345 and status = 3 and tags like  '%%NAT%%' or tags like '%%%s%%' or tags like '%%CUL%%' ORDER BY posted DESC;",(circle,))
        # Select the comments that haven't been archived.
        posttuple= self.c.fetchall()
        posts=[]
        for post in posttuple:
            posts.append(post)
        #calls = [i[0] for i in calls]
        userposts=[]
        for post in posts:
            if circle in post[1]:
                userposts.append(post)
                posts.remove(post)
                break;
        if len(userposts)==0:
            userposts.append(posts[0])
            posts.remove(posts[0])
        for post in posts:
            if "CUL" in post[1]:
                userposts.append(post)
                posts.remove(post)
                break;
        for post in posts:
            if "NAT" in post[1]:
                userposts.append(post)
                posts.remove(post)
                break;
        return userposts
    
