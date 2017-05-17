import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..','py_utils'))
from mongoDB import getCollection
from news_classifier_client import classify

def backfill(includeClass=True):
    newsCollection = getCollection()
    allNews = newsCollection.find({})
    count = 0
    for news in allNews:
        count += 1
        modified = False

        if count%50 == 0:
            print 'backfill on %i news' % count

        # correct news which doesn't have description
        if 'description' not in news or not news['description']:
            # title exist replace description with title
            if 'title' in news and news['title']:
                news['description'] = news['title']
                # add class to news
                if includeClass:
                    news['class'] = classify(news['title'])
                modified = True

            # url exist replace description with url
            elif 'url' in news and news['url']:
                news['description'] = news['url']
                if includeClass:
                    news['class'] = classify(news['url'])
                modified = True

            # text exist replace description with text
            elif 'text' in news and news['text']:
                news['description'] = news['text']
                if includeClass:
                    news['class'] = classify(news['text'])
                modified = True

            # otherwise leave description empty
            else:
                news['description'] = ''
        else:
            if includeClass:
                if 'title' in news and news['title']:
                    news['class'] = classify(news['title'])
                    modified = True
                elif 'url' in news and news['url']:
                    news['class'] = classify(news['url'])
                    modified = True
                elif 'text' in news and news['text']:
                    news['class'] = classify(news['text'])
                    modified = True
                else:
                    pass

        if modified:
            newsCollection.replace_one({'digest': news['digest']}, news, upsert=True)

    print 'backfill completed. %i news' % count



if __name__ == "__main__":
    backfill(includeClass=True)