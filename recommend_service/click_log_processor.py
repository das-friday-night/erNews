# -*- coding: utf-8 -*-

'''
Time decay model:

If selected:
p = (1-α)p + α

If not:
p = (1-α)p

Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''
from warnings import warn
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from config import QUE_LOGGER, SLEEP, TIME_DECAY_MODEL, NEWSCLASSES
from rabbitMQ import RabbitMQ
from mongoDB import getPreferences, getOneNews

logClient = RabbitMQ(QUE_LOGGER['URI'], QUE_LOGGER['NAME'])
alpha = TIME_DECAY_MODEL['ALPHA']

newsClasses = NEWSCLASSES['list']

def handler(log):
    if not isinstance(log, dict):
        warn('log processor dont handle broken log object')
        logClient.ackMessage()
        return

    if ('userID' not in log or 'newsID' not in log or 'timestamp' not in log):
        warn('log processor dont handle incompleted log object')
        logClient.ackMessage()
        return

    userID = log['userID']
    newsID = log['newsID']

    # ask if mongoDB has this user's preference model
    preferenceModel = list(getPreferences().find({'userID' : userID}))
    if len(preferenceModel) > 1:
        print warn('''one user can only have one preference model in database. 
                 something wrong with the preference model''')
        logClient.ackMessage()
        return
    elif len(preferenceModel) == 0:
        # if model not exist, create a new one
        print 'Creating preference model for new user: %s' % userID
        preferenceModel = {'userID' : userID}
        preference = {}
        p = 1.0/len(newsClasses)
        for newsClass in newsClasses:
            preference[newsClass] = float(p)
        preferenceModel['preference'] = preference
    else:
        print 'find existing preference model for user: %s' % userID
        preferenceModel = preferenceModel[0]

    print preferenceModel

    # update preference model
    # 1.ask mongoDB what class of this newsID
    news = getOneNews('digest', newsID)
    if (news is None 
        or 'class' not in news
        or news['class'] not in newsClasses):
        print news is None
        print 'class' not in news
        print news['class'] not in newsClasses
        warn("logger can't class attribute of news: %s" % newsID)
        logClient.ackMessage()
        return

    clickedClass = news['class']

    # 2. re-calculate preference model
    for newsClass in preferenceModel['preference']:
        p = preferenceModel['preference'][newsClass]
        if newsClass == clickedClass:
            preferenceModel['preference'][newsClass] = float((1.0 - alpha)*p + alpha)
        else:
            preferenceModel['preference'][newsClass] = float((1.0 - alpha)*p)

    # 3. update model in mongoDB
    getPreferences().replace_one({'userID' : userID}, preferenceModel, upsert=True)
    logClient.ackMessage()



while True:
    log = logClient.getMessage()
    if log is not None:
        try:
            handler(log)
        except Exception as e:
            print e
            pass
    # remove this, if this become a bottleneck
    logClient.sleep(SLEEP['LOGGER'])
