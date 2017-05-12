import news_cnn_model
import numpy as np
import os
import csv
import pandas as pd
import pickle
import shutil
import tensorflow as tf
from sklearn import metrics
from tensorflow.contrib.learn.python.learn.metric_spec import MetricSpec

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'model_test')
DATA_SET_FILE = os.path.join(os.path.dirname(__file__), '..', 'labeled_news_stem.csv')
VARS_FILE = os.path.join(os.path.dirname(__file__), '..', 'model_test/vars')
VOCAB_PROCESSOR_SAVE_FILE = os.path.join(os.path.dirname(__file__), '..', 'model_test/vocab_procesor_save_file')
N_CLASSES = 17

# # Training parms
# steps = 100
# docLength = 200
# iteration = 1
tf.logging.set_verbosity(tf.logging.INFO)


def loopFunction(steps, docLength, iteration):
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

    # Set up logging for predictions
    tensors_to_log = {"opt": "softmax"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=20)

    # validation monitor, log the metrics
    # https://www.tensorflow.org/get_started/monitors
    validation_metrics = {
        "accuracy" : MetricSpec(
            metric_fn=tf.contrib.metrics.streaming_accuracy, 
            prediction_key=learn.PredictionKey.CLASSES),
        "precision" : MetricSpec(
            metric_fn=tf.contrib.metrics.streaming_precision, 
            prediction_key=learn.PredictionKey.CLASSES)}

    validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(
        x_test,
        y_test,
        every_n_steps=11,
        metrics=validation_metrics)

    # Build model
    classifier = learn.SKCompat(learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR,
        config=learn.RunConfig(save_checkpoints_secs=None, save_checkpoints_steps=10)))

    # Train
    classifier.fit(x_train, y_train, steps=steps, monitors=[validation_monitor])

    # Evaluate model
    prediction = classifier.predict(x_test)
    y_predicted = prediction['classes']

    score = metrics.accuracy_score(y_test, y_predicted)
    # with open('night_test.csv','ab') as f:
    #     writer=csv.writer(f, delimiter=',')
    #     writer.writerow([iteration, steps, docLength, score])
    print('Accuracy: {0:f}'.format(score))


def main(unused_argv):
    # stepList = [400, 500, 600, 700]
    # doclenList = [100, 200, 300, 400, 500, 600]
    # totalIteration = len(stepList)*len(doclenList)*10
    # counter = 0
    # for oneStep in stepList:
    #     for oneDocLenth in doclenList:
    #         for i in range(10):
    #             counter += 1
    #             print "\n>>>>>>>>>>>>>>>>>>>>>(Outer) step=%i, (Inner) docLength=%i, %ith time" % (oneStep, oneDocLenth, i+1)
    #             loopFunction(oneStep, oneDocLenth, (i+1))
    #             print "\n>>>>>>>>>>>>>>>>>>>>>Complete %i/%i" % (counter, totalIteration)
    loopFunction(100, 100, (1))

if __name__ == '__main__':
    tf.app.run(main=main)