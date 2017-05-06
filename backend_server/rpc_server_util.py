import sys
import os
import pickle
import json
from bson.json_util import dumps
import redis
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
import mongoDB as mongoDB
from rabbitMQ import RabbitMQ
from config import REDIS, PAGINATION, QUE_LOGGER
from recommend_client import getUserPreferenceModel

redisClient = redis.StrictRedis(REDIS['HOST'], REDIS['PORT'])
logClient = RabbitMQ(QUE_LOGGER['URI'], QUE_LOGGER['NAME'])

def getNews(userID, pageID):
    pageID = int(pageID)
    # inclusive
    pageStartIndex = 0
    # exclusive
    pageEndIndex = PAGINATION
    if pageID>0:
        pageStartIndex = pageID*PAGINATION
        pageEndIndex = (pageID+1)*PAGINATION
    
    slicedNewsList = []
    if redisClient.get(userID) is not None:
        # redis save value in string, pickle.loads convert str to dict
        cachedNewsDigests = pickle.loads(redisClient.get(userID))
        # pageStartIndex > pageEndIndex: slicedDigests = []
        # pageStartIndex > len(cachedNewsDigests): slicedDigests = []
        slicedDigests = cachedNewsDigests[pageStartIndex : pageEndIndex]
        # slicedDigests = [], slicedNewsList = []
        slicedNewsList = list(mongoDB.getCollection().find({'digest': {'$in':slicedDigests}}))
    else:
        # TODO: all user get the same inital news, how to customize.
        pagesOfNews = list(mongoDB.getNews())
        cachedNewsDigests = map(lambda x:x['digest'], pagesOfNews)

        # save str to redis, pickle dumps convert dict to str
        redisClient.set(userID, pickle.dumps(cachedNewsDigests))
        redisClient.expire(userID, REDIS['DIGEST_EXPIRATION'])
        # pageStartIndex > pageEndIndex: slicedNewsList = []
        # pageStartIndex > len(cachedNewsDigests): slicedNewsList = []
        slicedNewsList = pagesOfNews[pageStartIndex : pageEndIndex]

    # TODO: preference model
    preferenceModel = getUserPreferenceModel()
    if preferenceModel is not None:
        print preferenceModel

    return json.loads(dumps(slicedNewsList))


def logNewsClick(userID, newsID):
    message = {
        'userID' : userID,
        'newsID' : newsID,
        'timestamp': str(datetime.utcnow())
    }
    logClient.sendMessage(message)
