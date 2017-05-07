# -*- coding: utf-8 -*-
import sys
import os
from warnings import warn
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from newspaper import Article

from config import QUE_MONITOR_SCRAPER, QUE_SCRAPER_DEDUPER, SLEEP
from rabbitMQ import RabbitMQ

monitorToScraperClient = RabbitMQ(QUE_MONITOR_SCRAPER['URI'], QUE_MONITOR_SCRAPER['NAME'])
scraperToDeduperClient = RabbitMQ(QUE_SCRAPER_DEDUPER['URI'], QUE_SCRAPER_DEDUPER['NAME'])

sleepTime = SLEEP['SCRAPER']
continuousMessageReceived = False

def handler(news):
    if news is None or not isinstance(news, dict):
        # news is broken need to be ignored
        monitorToScraperClient.ackMessage()
        warn('newspaper dont handle broken news object, news dropped')
        return

    article = Article(news['url'])
    article.download()
    # handle news url contains DOM that newspaper can't parse
    # reference: https://github.com/codelucas/newspaper/issues/143
    try:
        article.parse()
    except ValueError:
        monitorToScraperClient.ackMessage()
        warn('news scraper find %s contains bad xml node' % news['url'])
        return

    if article.text and article.text is not None:
        # print article.text
        news['text'] = article.text
        scraperToDeduperClient.sendMessage(news)
        monitorToScraperClient.ackMessage()
    else: 
        warn('newspaper parse no content from %s' % news['url'])
        monitorToScraperClient.ackMessage()


while True:
    news = monitorToScraperClient.getMessage()
    if news is not None:
        if continuousMessageReceived:
            if sleepTime > SLEEP['MIN']:
                sleepTime *= SLEEP['SCRAPER_DECREASE_RATE']
            else:
                sleepTime = SLEEP['MIN']
        else:
            sleepTime = SLEEP['SCRAPER']
            continuousMessageReceived = True
        try:
            handler(news)
        except Exception as e:
            print e
            pass
    else:
        continuousMessageReceived = False
        if sleepTime < SLEEP['MAX']:
            sleepTime *= SLEEP['SCRAPER_INCREASE_RATE']
        else:
            sleepTime = SLEEP['MAX']
    monitorToScraperClient.sleep(sleepTime)