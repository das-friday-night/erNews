# -*- coding: utf-8 -*-
import sys, os
import datetime
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from config import QUE_SCRAPER_DEDUPER, MONGO, TFIDF, SLEEP
from rabbitMQ import RabbitMQ
from mongoDB import getCollection

scraperToDeduperClient = RabbitMQ(QUE_SCRAPER_DEDUPER['URI'], QUE_SCRAPER_DEDUPER['NAME'])

def handler(news):
    if news is None or not isinstance(news, dict):
        print 'Warning: news deduper dont handle broken news object'
        scraperToDeduperClient.ackMessage()
        return
    if 'text' not in news or not news['text']:
        print 'Warning: news %s dont have content' % news['digest']
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
                print 'Warning: news deduper found news %s similar to existing one. Ignore.' % news['digest']
                scraperToDeduperClient.ackMessage()
                return

    # TODO: classify this news

    # similar news not found, save this news to database
    getCollection().replace_one({'digest': news['digest']}, news, upsert=True)
    scraperToDeduperClient.ackMessage()



while True:
    news = scraperToDeduperClient.getMessage()
    if news is not None:
        try:
            handler(news)
        except Exception as e:
            print e 
            pass
    scraperToDeduperClient.sleep(SLEEP['DEDUPER'])
