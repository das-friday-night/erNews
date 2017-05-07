# -*- coding: utf-8 -*-
import sys, os
import datetime
from dateutil import parser
from warnings import warn
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from config import QUE_SCRAPER_DEDUPER, MONGO, TFIDF, SLEEP
from rabbitMQ import RabbitMQ
from mongoDB import getCollection
from news_classifier_client import classify

scraperToDeduperClient = RabbitMQ(QUE_SCRAPER_DEDUPER['URI'], QUE_SCRAPER_DEDUPER['NAME'])
sleepTime = SLEEP['DEDUPER']
continuousMessageReceived = False

def handler(news):
    if news is None or not isinstance(news, dict):
        warn('news deduper dont handle broken news object')
        scraperToDeduperClient.ackMessage()
        return
    if 'text' not in news or not news['text']:
        warn('news %s dont have content' % news['digest'])
        scraperToDeduperClient.ackMessage()
        return

    # prepare date and time to a format Mongo accept
    news['publishedAt'] = parser.parse(news['publishedAt'])
    # parse news publish date
    publishedTime = news['publishedAt']
    publishedDayBegin = datetime.datetime(publishedTime.year, publishedTime.month, publishedTime.day, 0, 0, 0, 0)
    publishedDayEnd = publishedDayBegin + datetime.timedelta(days=1)

    # get same day news from mongoDB
    newsListOnThatDay = list(getCollection().find({'publishedAt': {'$gte': publishedDayBegin, '$lt': publishedDayEnd}}))
    if newsListOnThatDay is not None and len(newsListOnThatDay)>0:
        # Python: List Comprehensions
        newsArray = [str(newsOnThatDay['text'].encode('utf-8')) for newsOnThatDay in newsListOnThatDay]
        newsArray.insert(0, news['text'])

        # calc tfidf of all same day news
        tfidf = TfidfVectorizer().fit_transform(newsArray)
        firstDoc_sim = tfidf[0] * tfidf.T

        _,colSize = firstDoc_sim.shape

        # drop this news if found similar news in history
        for col in range(1, colSize):
            if firstDoc_sim[0, col] > TFIDF['SAME_NEWS_SIMILARITY_THRESHOLD']:
                warn('news deduper found news %s similar to existing one. Ignore.' % news['digest'])
                scraperToDeduperClient.ackMessage()
                return

    # data cleaning on news description: 
    # Reason:  we need description for news classifier service, more specificly, 
    #          for machine learning
    # Problem: some news don't have description, will cause vocabulary_processor to crash.
    # Solution: try to fill description with title, if title missing, fill with text
    if 'description' not in news or not news['description']:
        if 'title' in news and news['title']:
            news['description'] = news['title']
        else:
            news['description'] = news['text']

    # classify this news
    if 'title' in news:
        news['class'] = classify(news['title'])

    # similar news not found, save this news to database
    getCollection().replace_one({'digest': news['digest']}, news, upsert=True)
    scraperToDeduperClient.ackMessage()



while True:
    news = scraperToDeduperClient.getMessage()
    if news is not None:
        if continuousMessageReceived:
            if sleepTime > SLEEP['MIN']:
                sleepTime *= SLEEP['DEDUPER_DECREASE_RATE']
            else:
                sleepTime = SLEEP['MIN']
        else:
            sleepTime = SLEEP['DEDUPER']
            continuousMessageReceived = True
        try:
            handler(news)
        except Exception as e:
            print e 
            pass
    
    else: 
        continuousMessageReceived = False
        if sleepTime < SLEEP['MAX']:
            sleepTime *= SLEEP['DEDUPER_INCREASE_RATE']
        else:
            sleepTime = SLEEP['MAX']
    scraperToDeduperClient.sleep(sleepTime)
