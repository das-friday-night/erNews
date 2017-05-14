import sys
import os
import operator
import pickle
import json
from bson.json_util import dumps
import redis
from datetime import datetime
import yaml
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
import mongoDB as mongoDB
from rabbitMQ import RabbitMQ
from recommend_client import getUserPreferenceModel

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
REDIS = config['REDIS']
PAGINATION = config['PAGINATION']
QUE_LOGGER = config['QUE_LOGGER']
NEWSCLASSES = config['NEWSCLASSES']['list']

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
    preferenceModel = getUserPreferenceModel(userID)
    if preferenceModel is not None:
        print "preferenceModel is not use yet"

    # convert publishedAt to string
    # print slicedNewsList[0]['publishedAt'].strftime('%Y-%m-%d %H:%M')
    for newsObj in slicedNewsList:
        newsTime = newsObj['publishedAt']
        strTime = newsTime.strftime('%Y-%m-%d %H:%M')
        newsObj['publishedAt'] = strTime.decode('utf-8')

    return json.loads(dumps(slicedNewsList))


def logNewsClick(userID, newsID):
    message = {
        'userID' : userID,
        'newsID' : newsID,
        'timestamp': str(datetime.utcnow())
    }
    logClient.sendMessage(message)


"""
newsDistribution: 
{
    chart: {
        type: 'bar'
    },
    title: {
        text: 'News Distribution By Class'
    },
    xAxis: {
        categories: ['Apples', 'Bananas', 'Oranges']
    },
    yAxis: {
        title: {
            text: 'News Amount'
        }
    },
    series: [{
        name: 'Jane',
        data: [1, 0, 4]
    }, {
        name: 'John',
        data: [5, 7, 3]
    }]
}
"""
def getNewsDistribution():
    classAmountDict = {}
    for newsClass in NEWSCLASSES:
        amount = mongoDB.getCollection().find({'class':newsClass}).count()
        classAmountDict[newsClass] = amount
    classAmountList = sorted(classAmountDict.items(), key=operator.itemgetter(1), reverse=True)
    classes = [pair[0] for pair in classAmountList]
    amount = [pair[1] for pair in classAmountList]
    newsDistribution = {
        'newsDistribution' : {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': 'News Distribution By Class'
            },
            'xAxis': {
                'categories': classes
            },
            'yAxis': {
                'title': {
                    'text': 'News Amount'
                }
            },
            'series': [{
                'data': amount
            }],
            'legend': {
                'enabled': False
            }
        }
    }
    return json.loads(dumps(newsDistribution))
