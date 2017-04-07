from pymongo import MongoClient

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
DB_NAME = 'erNews'

client = MongoClient("%s:%s" % (MONGO_HOST, MONGO_PORT))

def get(db=DB_NAME):
    db = client[db]
    count = db['news'].count()   
    return count
