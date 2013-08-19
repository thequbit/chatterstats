from twitter import *
from cfgfile import parseconfig

def getauth():
    settings = parseconfig('twitterauth.ini')
    return settings

def init():
    settings = getauth()
    t = Twitter(
                auth=OAuth(settings['OAUTH_TOKEN'],settings['OAUTH_SECRET'],
                           settings['CONSUMER_KEY'],settings['CONSUMER_SECRET'])
               )
    return t

def gettweets(lat,lng,radius="20mi",count=100):
    t = init()
    geocode = "{0},{1},{2}".format(lat,lng,radius)
    results = t.search.tweets(q="#roc",geocode=geocode,count=count)
    hashtags = {}
    tweets = []
    success = True
    try:
        for status in results['statuses']:
            sn = status['user']['screen_name']
            tid = status['id']
            text = status['text']
            created = status['created_at']
            tweets.append((sn,tid,text,created))
            for tag in status['entities']['hashtags']:
                if tag['text'] in hashtags:
                    hashtags[tag['text']] += 1
                else:
                    hashtags[tag['text']] = 1
    except:
        success = False
    return tweets,success
