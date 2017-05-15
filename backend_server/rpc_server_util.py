import sys
import os
import operator
import pickle
import math
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
NEWSSOURCES = config['NEWSAPI']['DEFAULT_SOURCES']

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
        strTime = datetime.strftime(newsTime, '%Y-%m-%d %H:%M')
        newsObj['publishedAt'] = strTime.decode('utf-8')

    return json.loads(dumps(slicedNewsList))


def logNewsClick(userID, newsID):
    message = {
        'userID' : userID,
        'newsID' : newsID,
        'timestamp': str(datetime.utcnow())
    }
    logClient.sendMessage(message)



def getNewsDistribution():
    # compute distribution based on class
    classAmountDict = {}
    for newsClass in NEWSCLASSES:
        amount = mongoDB.getCollection().find({'class':newsClass}).count()
        classAmountDict[newsClass] = amount
    classAmountList = sorted(classAmountDict.items(), key=operator.itemgetter(1), reverse=True)
    classes = [pair[0] for pair in classAmountList]
    classAmounts = [pair[1] for pair in classAmountList]

    # compute distribution based on source
    sourceAmountDict = {}
    for source in NEWSSOURCES:
        amount = mongoDB.getCollection().find({'source':source}).count()
        sourceAmountDict[source] = amount
    sourceAmountList = sorted(sourceAmountDict.items(), key=operator.itemgetter(1), reverse=True)
    # sourceAmountList = [('six', 6), ('six2', 6), ('two', 2), ('one', 1)]

    datalist = []
    total = sum([pair[1] for pair in sourceAmountList])
    remin = 100.0
    for source in sourceAmountList:
        percentile = float(source[1])/total*100
        percentile = math.floor(percentile*10)/10
        print "%s: %f" % (source[0],percentile)
        if percentile < 7.6:
            remin = math.floor(remin*10)/10
            datalist.append({'name': 'other sources', 'y':remin})
            break
        else:
            datalist.append({'name': source[0], 'y': percentile})
            remin = remin - percentile

    newsDistribution = {
        'class' : {
            'chart': {
                'type': 'column'
            },
            'title': {
                'text': 'News Distribution By Class'
            },
            'xAxis': {
                'categories': classes,
                'labels': {'style': {
                    'fontFamily': 'Verdana, sans-serif',
                    'fontSize': '13px'
                    }}
            },
            'yAxis': {
                'title': {
                    'text': 'News Amount'
                }
            },
            'series': [{
                'data': classAmounts
            }],
            'legend': {
                'enabled': False
            },
            'credits': {
                'enabled': False
            },
        },
        'source' : {
            'chart': {
                'plotBackgroundColor': None,
                'plotBorderWidth': None,
                'plotShadow': False,
                'type': 'pie'
            },
            'title': {
                'text': 'news distribution by news sources'
            },
            'tooltip': {
                'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            'plotOptions': {
                'pie': {
                    'allowPointSelect': True,
                    'cursor': 'pointer',
                    'dataLabels': {'enabled': False},
                    'showInLegend': True
                }
            },
            'series': [{
                'name': 'source',
                'colorByPoint': 'true',
                'data': datalist
            }]
        }
    }

    return json.loads(dumps(newsDistribution))
