import json

from pymongo import MongoClient
from bson.json_util import dumps
from config import MONGO

HOST = MONGO['HOST']
PORT = MONGO['PORT']
DB = MONGO['NEWS_DB']
COLLECTION = MONGO['NEWS_COLLECTION']

client = MongoClient("%s:%s" % (HOST, PORT))

def getCount(db=DB, collection=COLLECTION):
    db = client[db]
    count = db[collection].count()   
    return count

def getNews(db=DB, collection=COLLECTION):
    db = client[db]
    news = db[collection].find(limit=10)
    news = list(news)
    news = dumps(news)
    return json.loads(news)

def getCollection(db=DB, collection=COLLECTION):
    db = client[db]
    return db[collection]