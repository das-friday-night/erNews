# -*- coding: utf-8 -*-
import sys
import os
import hashlib
from datetime import datetime
import redis
import yaml
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from rabbitMQ import RabbitMQ
from newsapi_client import getNewsFromNewsAPI

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
QUE_MONITOR_SCRAPER = config['QUE_MONITOR_SCRAPER']
REDIS = config['REDIS']
SLEEP = config['SLEEP']

# set up rabbitMQ between monitor and scraper
mqClient = RabbitMQ(QUE_MONITOR_SCRAPER['URI'], QUE_MONITOR_SCRAPER['NAME'])

# set up redis store new news for one day
redisClient = redis.StrictRedis(REDIS['HOST'], REDIS['PORT'])

sleepTime = SLEEP['MONITOR']
continuousMessageReceived = False

while True: 
    newslist = getNewsFromNewsAPI()
    if(newslist):
        if continuousMessageReceived:
            if sleepTime > SLEEP['MIN']:
                sleepTime *= SLEEP['MONITOR_DECREASE_RATE']
            else:
                sleepTime = SLEEP['MIN']
        else:
            sleepTime = SLEEP['MONITOR']
            continuousMessageReceived = True

        newsAmount = 0
        for news in newslist:
            digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')
            # if we never seen this news in past day
            if redisClient.get(digest) is None:
                news['digest'] = digest
                newsAmount = newsAmount + 1
                if news['publishedAt'] is None:
                    # format: YYYY-MM-DDTHH:MM:SS in UTC
                    news['publishedAt'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                redisClient.set(digest, news)
                redisClient.expire(digest, REDIS['NEWS_EXPIRATION'])
                mqClient.sendMessage(news)
            # if we seen this news in past day, ignore it.

        print 'fetched %d new news.' % newsAmount

    else:
        continuousMessageReceived = False
        if sleepTime < SLEEP['MAX']:
            sleepTime *= SLEEP['MONITOR_INCREASE_RATE']
        else:
            sleepTime = SLEEP['MAX']
    mqClient.sleep(sleepTime)
