import time
import dateutil.parser
import re
from gettweets import gettweets
from db.tweets import tweets as db_tweets

def getcreds():
    creds = {}
    configfile = "sqlcreds.txt"
    f = open(configfile)
    for line in f:
        m = re.search('^\s*#', line)
        if m:
            continue
        m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
        if m is None:
            continue
        creds[m.group(1)] = m.group(2)
    f.close()
    return creds

def sanitize(txt):
    txt = txt.encode('utf-8')
    return txt

def savetweets(db,tweets):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    for tweet in tweets:
        sn,tid,text,created = tweet
        text = sanitize(text)
        dt = dateutil.parser.parse(created)
        tweetid,c = db.add_ine(sn,tid,text,dt,now)
        if c == 1:
            count += 1
    return count

def main():

    print "[INFO   ] Running ..."

    # 20 mile radius of Rochester, NY
    lat="43.1547"
    lng="-77.6158"
    radius="20mi"
    count = 100

    creds = getcreds()
    db = db_tweets(creds['host'],creds['username'],
                   creds['password'],creds['database'])

    # every minute grab the last 100 tweets from the radius of the lat and lng
    while True:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print "[TIME   ] --- {0} ---".format(now)
        print "[INFO   ] Grabing latest tweets ..."
        tweets,success = gettweets(lat=lat,lng=lng,radius=radius,count=count)
        if success:
            print "[INFO   ] Processing {0} tweets ..."
            count = savetweets(db,tweets)
            print "[INFO   ] Saved {0} of the {1} tweets.".format(count,len(tweets))
        time.sleep(60)

main()
