import sys
import os
import operator
import pickle
import math
import json
from collections import deque
from datetime import datetime
from bson.json_util import dumps
from warnings import warn
import redis
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
UNCLASSIFIED_RATIO = config['RECOMMEND_SERVER']['UNCLASSIFIED_RATIO']

redisClient = redis.StrictRedis(REDIS['HOST'], REDIS['PORT'])
logClient = RabbitMQ(QUE_LOGGER['URI'], QUE_LOGGER['NAME'])

def reorderPagesOfNews(userID, pagesOfNews):
    # pagesOfNews: a list of news dict obj
    # preferenceModel: a list of new class high -> low preference. e.g:
    """[u'Technology', u'Weather', u'Politics & Government', u'Entertainment', u'Media',
    u'Colleges & Schools', u'Advertisements', u'Sports', u'Religion', u'Magazine', u'Other',
    u'Traffic', u'Regional News', u'Economic & Corp', u'World', u'Crime', u'Environmental']"""
    preferenceModel, preferenceRatioList = getUserPreferenceModel(userID)
    if preferenceModel is not None:
        classNewsHolder = {}
        for news in pagesOfNews:
            if 'class' in news:
                classNewsHolder.setdefault(news['class'], []).append(news)
            else:
                # news with no class
                classNewsHolder.setdefault('unclassified', []).append(news)

        pagesOfNews = []
        preferenceModel.append('unclassified')
        for newsClass in preferenceModel:
            if newsClass in classNewsHolder:
                pagesOfNews.extend(classNewsHolder[newsClass])

    return pagesOfNews
    # -----------------------------------------------------
    if preferenceModel is not None 
        and preferenceRatioList is not None 
        and len(preferenceModel) == len(preferenceRatioList):
        # create a dict of queue to hold news from different classes
        newsClassQueueHolder = {}
        for news in pagesOfNews:
            if 'class' in news:
                # news with class attribute
                newsClassQueueHolder.setdefault(news['class'], deque()).append(news)
            else:
                # news with no class
                newsClassQueueHolder.setdefault('unclassified', deque()).append(news)
        
        # set up variable and append unclassified to preferenceModel and preferenceRatioList if needed
        counter = len(pagesOfNews)
        emptyQueueList = []
        returnNewsList = []
        if len(newsClassQueueHolder['unclassified']) != 0:
            preferenceModel.append('unclassified')
            preferenceRatioList.append(UNCLASSIFIED_RATIO)
        while counter > 0:
            for newsClass, preferenceRatio in zip(preferenceModel, preferenceRatioList):
                # check if queue has enough item to pop, if not enough, pop reminder
                queueSize = len(newsClassQueueHolder[newsClass])
                if queueSize <= preferenceRatio:
                    # delete corresponding item in preferenceModel & preferenceRatioList
                    # make sure deleltion here won't affect code after
                    emptyQueueList.append({'newsClass' : newsClass, 'preferenceRatio' : preferenceRatio}))
                    preferenceRatio = queueSize

                for i in range(preferenceRatio):
                    newsClassQueueHolder[newsClass].popleft()
                    counter = counter - 1
            
            for emptyQueue in emptyQueueList:
                preferenceModel.remove(emptyQueue['newsClass'])
                preferenceModel.remove(emptyQueue['preferenceRatio'])

        return returnNewsList
    else:
        # if something goes wrong, return the original pagesOfNews
        warn("""preferenceModel is None:%r, preferenceRatioList is None:%r, len(preferenceModel)!=len(preferenceRatioList):%r""" 
                % (preferenceModel is None, preferenceRatioList is None, len(preferenceModel) != len(preferenceRatioList)))
        return pagesOfNews


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
        pagesOfNews = list(mongoDB.getNews())
        # reorder news based on preference model
        pagesOfNews = reorderPagesOfNews(userID, pagesOfNews)
        cachedNewsDigests = map(lambda x:x['digest'], pagesOfNews)
        # print cachedNewsDigests

        # save str to redis, pickle dumps convert dict to str
        redisClient.set(userID, pickle.dumps(cachedNewsDigests))
        redisClient.expire(userID, REDIS['DIGEST_EXPIRATION'])
        # pageStartIndex > pageEndIndex: slicedNewsList = []
        # pageStartIndex > len(cachedNewsDigests): slicedNewsList = []
        slicedNewsList = pagesOfNews[pageStartIndex : pageEndIndex]

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


# this is for chart drawing
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
        # print "%s: %f" % (source[0],percentile)
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
