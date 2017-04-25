RPC_SERVER = {
    'HOST': 'localhost',
    'PORT': 4040
}

MONGO = {
    'HOST': 'localhost',
    'PORT': '27017',
    'DB_NAME': 'erNews'
}

NEWSAPI = {
    'KEY': '4ed99fbbbee04fdb9b1a8426882682cc',
    'API_BASE': 'https://newsapi.org/v1/articles',
    'DEFAULT_SOURCES': ['the-new-york-times'],
    'DEFUALT_SORT': 'top'
}

QUE_MONITOR_SCRAPER = {
    'URI': 'amqp://uneggxcr:eElS-gADqt1sv8niqv6uzKaiCKT2mnhP@donkey.rmq.cloudamqp.com/uneggxcr',
    'NAME': 'monitor_scraper',
    'SLEEP_SECONDS': 10
}

QUE_SCRAPER_DEDUPER = {
    'URI': 'amqp://llkcvaiq:98buUaysrg1umBoqAdVRfb9nAngHtsxq@donkey.rmq.cloudamqp.com/llkcvaiq',
    'NAME': 'scraper_deduper',
    'SLEEP_SECONDS': 5
}

REDIS = {
    'HOST': 'localhost',
    'PORT': 6379,
    'NEWS_EXPIRATION': 3600*24
}
