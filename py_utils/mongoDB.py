import json

import os
import pymongo
import yaml
from bson.json_util import dumps

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
MONGO = config['MONGO']
DB = MONGO['NEWS_DB']
COLLECTION = MONGO['NEWS_COLLECTION']

client = pymongo.MongoClient("%s:%s" % (MONGO['HOST'], MONGO['PORT']))

def getCount(db=DB, collection=COLLECTION):
    db = client[db]
    count = db[collection].count()   
    return count

def getNews(db=DB, collection=COLLECTION):
    # TODO: use getCollection()
    db = client[db]
    news = db[collection].find().sort('publishedAt', pymongo.DESCENDING).limit(MONGO['FIND_AMOUNT'])
    news = list(news)
    news = dumps(news)
    return json.loads(news)

def getOneNews(key, val):
    return getCollection().find_one({key : val})

def getCollection(db=DB, collection=COLLECTION):
    db = client[db]
    return db[collection]

def getPreferences(db=MONGO['USER_DB'], collection=MONGO['USER_PREFERENCES']):
    db = client[db]
    return db[collection]