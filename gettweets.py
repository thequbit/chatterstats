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

def main():
    t = init()

    lat="43.1547"
    lng="-77.6158"
    radius="20mi"
    geocode = "{0},{1},{2}".format(lat,lng,radius)

    print "Getting tweets for Monroe County ..."

    # lat long of Rochester, NY
    results = t.search.tweets(q="#roc",geocode=geocode,count=100)

    print "Processing {0} tweets ...".format(len(results['statuses']))

    hashtags = {}
    tweets = []
    for status in results['statuses']:
        tweet = (status['id'],status['text'])
        tweets.append(tweet)
        for tag in status['entities']['hashtags']:
            if tag['text'] in hashtags:
                hashtags[tag['text']] += 1
            else:
                hashtags[tag['text']] = 1

    print "{0} tweets and {1} hashtags successfully processed.".format(len(tweets),len(hashtags))

main()
