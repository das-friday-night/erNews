# -*- coding: utf-8 -*-
import pyjsonrpc
import pickle
import os
import sys
import time
import yaml
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from trainer.news_cnn_model import generate_cnn_model
from news_csv_cleaner import classDetect
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
NEWS_CLASSIFIER_SERVER = config['NEWS_CLASSIFIER_SERVER']
NEWSCLASSES = config['NEWSCLASSES']

VOCAB_PROCESSOR_DIR = os.path.join(os.path.dirname(__file__), 'model/vocab_procesor_save_file')
VARS_FILE = os.path.join(os.path.dirname(__file__), 'model/vars')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model') 
MODEL_UPDATE_LAG_IN_SECONDS = 10

learn = tf.contrib.learn
newsClasses = NEWSCLASSES['map']
vocab_processor = None
classifier = None

def loadVocabAndModel():
    # load vocab_processor
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(VOCAB_PROCESSOR_DIR)
    # load classifier
    n_words = 0
    with open(VARS_FILE, 'r') as f:
        n_words = pickle.load(f)
    global classifier
    classifier = learn.SKCompat(learn.Estimator(
        model_fn=generate_cnn_model(len(newsClasses), n_words),
        model_dir=MODEL_DIR))

    # Prepare training and testing
    df = pd.read_csv('labeled_news.csv', header=None)

    train_df = df[0:1]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.score(x_train, y_train)
    print "Updated complete."

class OnModelChange(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print "Model update detected. Loading new model."
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        loadVocabAndModel()

# setup watchdog
fsDaemon = Observer()
fsDaemon.schedule(OnModelChange(), path=MODEL_DIR, recursive=False)
fsDaemon.start()

# set up classifier model
loadVocabAndModel()

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def classify(self, text):
        # first predict via corpus
        prediction = classDetect(text)
        # if can't predict, use machine learning method
        if prediction == '0':
            text_series = pd.Series([text])
            vocabTransformation = np.array(list(vocab_processor.transform(text_series)))
            prediction = classifier.predict(vocabTransformation)
            prediction = str(prediction['classes'][0])
        
        prediction = newsClasses[prediction]
        return prediction

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (NEWS_CLASSIFIER_SERVER['HOST'], NEWS_CLASSIFIER_SERVER['PORT']),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://%s:%d" % (NEWS_CLASSIFIER_SERVER['HOST'], NEWS_CLASSIFIER_SERVER['PORT'])
http_server.serve_forever()
