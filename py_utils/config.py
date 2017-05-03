RPC_SERVER = {
    'HOST': 'localhost',
    'PORT': 4040
}

RECOMMEND_SERVER = {
    'HOST': 'localhost',
    'PORT': 5050
}

MONGO = {
    'HOST': 'localhost',
    'PORT': '27017',
    'FIND_AMOUNT': 100,
    'NEWS_DB': 'test',
    'NEWS_COLLECTION': 'news',
    'USER_DB': 'user',
    'USER_PREFERENCES': 'preferences'
}

NEWSAPI = {
    'KEY': '4ed99fbbbee04fdb9b1a8426882682cc',
    'API_BASE': 'https://newsapi.org/v1/articles',
    'DEFAULT_SOURCES': ['the-new-york-times'],
    'DEFUALT_SORT': 'top'
}

QUE_MONITOR_SCRAPER = {
    'URI': 'amqp://uneggxcr:eElS-gADqt1sv8niqv6uzKaiCKT2mnhP@donkey.rmq.cloudamqp.com/uneggxcr',
    'NAME': 'monitor_scraper'
}

QUE_SCRAPER_DEDUPER = {
    'URI': 'amqp://llkcvaiq:98buUaysrg1umBoqAdVRfb9nAngHtsxq@donkey.rmq.cloudamqp.com/llkcvaiq',
    'NAME': 'scraper_deduper'
}

QUE_LOGGER = {
    'URI': 'amqp://siodttgr:2oPzhSjBUG0nZSz9hJnSg5a1b1TUIZN0@donkey.rmq.cloudamqp.com/siodttgr',
    'NAME': 'logger'
}

SLEEP = {
    'MONITOR': 60,
    'SCRAPER': 5,
    'DEDUPER': 5,
    'LOGGER' : 1
}

PAGINATION = 10

REDIS = {
    'HOST': 'localhost',
    'PORT': 6379,
    'NEWS_EXPIRATION': 3600*24,
    'DIGEST_EXPIRATION': 600
}

TFIDF = {
    'SAME_NEWS_SIMILARITY_THRESHOLD': 0.85
}

TIME_DECAY_MODEL = {
    'ALPHA' : 0.1
}