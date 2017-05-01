import json

import pymongo
from bson.json_util import dumps
from config import MONGO

DB = MONGO['NEWS_DB']
COLLECTION = MONGO['NEWS_COLLECTION']

client = pymongo.MongoClient("%s:%s" % (MONGO['HOST'], MONGO['PORT']))

def getCount(db=DB, collection=COLLECTION):
    db = client[db]
    count = db[collection].count()   
    return count

def getNews(db=DB, collection=COLLECTION):
    db = client[db]
    news = db[collection].find().sort('publishedAt', pymongo.DESCENDING).limit(MONGO['FIND_AMOUNT'])
    news = list(news)
    news = dumps(news)
    return json.loads(news)

def getCollection(db=DB, collection=COLLECTION):
    db = client[db]
    return db[collection]