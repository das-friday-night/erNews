import json

from pymongo import MongoClient
from bson.json_util import dumps
from config import MONGO

MONGO_HOST = MONGO['HOST']
MONGO_PORT = MONGO['PORT']
DB_NAME = MONGO['DB_NAME']

client = MongoClient("%s:%s" % (MONGO_HOST, MONGO_PORT))

def getCount(db=DB_NAME):
    db = client[db]
    count = db['news'].count()   
    return count

def getNews(db=DB_NAME):
    db = client[db]
    news = db['news'].find(limit=10)
    news = list(news)
    news = dumps(news)
    return json.loads(news)

