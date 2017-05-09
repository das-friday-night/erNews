import news_cnn_model
import numpy as np
import os
import csv
import pandas as pd
import pickle
import shutil
import tensorflow as tf
from sklearn import metrics

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')
DATA_SET_FILE = os.path.join(os.path.dirname(__file__), '..', 'labeled_news_stem.csv')
VARS_FILE = os.path.join(os.path.dirname(__file__), '..', 'model/vars')
VOCAB_PROCESSOR_SAVE_FILE = os.path.join(os.path.dirname(__file__), '..', 'model/vocab_procesor_save_file')
N_CLASSES = 17

# Training parms
steps = 100
docLength = 200
iteration = 1

def loopFunction():
    if REMOVE_PREVIOUS_MODEL:
        if os.path.exists(MODEL_OUTPUT_DIR):
            # Remove old model
            shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)


    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:700]
    # x - news title, y - class
    x_train = train_df[1]
    # y_train [1, entry amount in x_train]
    y_train = train_df[0]

    test_df = df.drop(train_df.index)
    x_test = test_df[1]
    y_test = test_df[0]

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(docLength)
    # fit_transform: vocab_processor recognize words in x_train
    # x_train [entry amount in x_train, MAX_DOCUMENT_LENGTH]
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    # transform: vocab_processor only mark words in x_test only appeared in x_train
    # x_test [entry amount in x_test, MAX_DOCUMENT_LENGTH]
    x_test = np.array(list(vocab_processor.transform(x_test)))

    # unique words amount in x_train
    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    # Saving n_words and vocab_processor:
    with open(VARS_FILE, 'w') as f:
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=steps)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    with open('night_test.csv','ab') as f:
        writer=csv.writer(f, delimiter=',')
        writer.writerow([iteration, steps, docLength, score])
    print('Accuracy: {0:f}'.format(score))


def main(unused_argv):
    stepList = [100, 200, 300, 400, 500, 600, 700]
    doclenList = [100, 200, 300, 400, 500, 600]
    totalIteration = len(stepList)*len(doclenList)*4
    counter = 0
    for oneStep in stepList:
        steps = oneStep
        for oneDocLenth in doclenList:
            docLength = oneDocLenth
            for i in range(10):
                counter += 1
                iteration = i+1
                print "\n>>>>>>>>>>>>>>>>>>>>>(Outer) step=%i, (Inner) docLength=%i, %ith time" % (steps, docLength, iteration)
                loopFunction()
                print "\n>>>>>>>>>>>>>>>>>>>>>Complete %i/%i" % (counter, totalIteration)

if __name__ == '__main__':
    tf.app.run(main=main)


