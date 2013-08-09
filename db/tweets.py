import MySQLdb as mdb
import _mysql as mysql
import re

class tweets:

    __settings = {}
    __con = False

    def __init__(self,host,user,passwd,db):
        self.__settings['host'] = host
        self.__settings['username'] = user
        self.__settings['password'] = passwd
        self.__settings['database'] = db
    def __connect(self):
        con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'],
                          passwd=self.__settings['password'], db=self.__settings['database'])
        return con

    def __sanitize(self,valuein):
        if type(valuein) == 'str':
            valueout = mysql.escape_string(valuein)
        else:
            valueout = valuein
        return valuein

    def add(self,username,id,text,created,pulldt):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO tweets(username,id,text,created,pulldt) VALUES(%s,%s,%s,%s,%s)",(self.__sanitize(username),self.__sanitize(id),self.__sanitize(text),self.__sanitize(created),self.__sanitize(pulldt)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,tweetid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM tweets WHERE tweetid = %s",(tweetid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM tweets")
            rows = cur.fetchall()
            cur.close()
        _tweets = []
        for row in rows:
            _tweets.append(row)
        con.close()
        return _tweets

    def delete(self,tweetid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM tweets WHERE tweetid = %s",(tweetid))
            cur.close()
        con.close()

    def update(self,tweetid,username,id,text,created,pulldt):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE tweets SET username = %s,id = %s,text = %s,created = %s,pulldt = %s WHERE tweetid = %s",(self.__sanitize(username),self.__sanitize(id),self.__sanitize(text),self.__sanitize(created),self.__sanitize(pulldt),self.__sanitize(tweetid)))
            cur.close()
        con.close()

##### Application Specific Functions #####

    # add if not exists
    def add_ine(self,username,id,text,created,pulldt):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO tweets(username,id,text,created,pulldt)
                           SELECT * FROM (SELECT %s,%s,%s,%s,%s) as tmp
                           WHERE NOT EXISTS (
                               SELECT id FROM tweets WHERE id = %s
                           ) LIMIT 1""",
                        (self.__sanitize(username),self.__sanitize(id),self.__sanitize(text),self.__sanitize(created),self.__sanitize(pulldt),self.__sanitize(id))
                       )
            cur.close()
            newid = cur.lastrowid
            count = cur.rowcount
        con.close()
        return newid,count

    def getlast24hours(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT text FROM tweets WHERE pulldt >= now() - INTERVAL 1 DAY;")
            rows = cur.fetchall()
            cur.close()
        _tweets = []
        for row in rows:
            _tweets.append(row[0])
        con.close()
        return _tweets

