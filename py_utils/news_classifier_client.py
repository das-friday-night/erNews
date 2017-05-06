# -*- coding: utf-8 -*-
import pyjsonrpc
from config import NEWS_CLASSIFIER_SERVER

url = 'http://%s:%i' % (NEWS_CLASSIFIER_SERVER['HOST'], NEWS_CLASSIFIER_SERVER['PORT'])
client = pyjsonrpc.HttpClient(url=url)

def classify(text):
    return client.call('classify', text)
