import os 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..','py_util/config'))
from mongoDB import getCollection
from news_classifier_client import classify

newsCollection = getCollection()
allNews = newsCollection.find({})
count = 0
for news in allNews:
    count += 1
    if 'title' in news:
        news['class'] = classify(news['title'])
        newsCollection.replace_one({'digest': news['digest']}, news, upsert=True)

