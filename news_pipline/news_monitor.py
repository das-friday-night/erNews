# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import redis
import hashlib
import datetime
from py_utils.config import QUE_MONITOR_SCRAPER, REDIS, SLEEP
from py_utils.rabbitMQ import RabbitMQ
from py_utils.newsapi_client import getNewsFromNewsAPI

# set up rabbitMQ between monitor and scraper
mqClient = RabbitMQ(QUE_MONITOR_SCRAPER['URI'], QUE_MONITOR_SCRAPER['NAME'])

# set up redis store new news for one day
redisClient = redis.StrictRedis(REDIS['HOST'], REDIS['PORT'])

# TODO: add complete news source to getNewsFromNewsAPI()

while True: 
    newslist = getNewsFromNewsAPI()
    if(newslist):
        newsAmount = 0
        for news in newslist:
            digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')
            if redisClient.get(digest) is None:
                news['digest'] = digest
                newsAmount = newsAmount + 1
                if news['publishedAt'] is None:
                    # format: YYYY-MM-DDTHH:MM:SS in UTC
                    news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                redisClient.set(digest, news)
                redisClient.expire(digest, REDIS['NEWS_EXPIRATION'])

                mqClient.sendMessage(news)
        print 'fetched %d new news.' % newsAmount
    mqClient.sleep(SLEEP['MONITOR'])