# -*- coding: utf-8 -*-
import pyjsonrpc
import os
import yaml

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
NEWS_CLASSIFIER_SERVER = config['NEWS_CLASSIFIER_SERVER']

url = 'http://%s:%i' % (NEWS_CLASSIFIER_SERVER['HOST'], NEWS_CLASSIFIER_SERVER['PORT'])
client = pyjsonrpc.HttpClient(url=url)

def classify(text):
    return client.call('classify', text)
