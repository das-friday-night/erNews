from rpc_server_util import reorderPagesOfNews
# from sets import Set

# page1 = getNews('xiaoming2', 0)
# print page1
# page2 = getNews('XiaoWang', 1)

# print 'page1: %i' % len(page1)
# print 'page2: %i' % len(page2)

# page_1_set = Set([news['digest'] for news in page1])
# page_2_set = Set([news['digest'] for news in page2])

# assert len(page_1_set.intersection(page_2_set)) == 0

# print 'test pass'

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
import mongoDB as mongoDB
from recommend_client import getUserPreferenceModel

preference = getUserPreferenceModel('a@b.com')
if preference:
    exit
    
preferenceModel = preference["newsClassNameList"]
preferenceRatioList = preference["newsClassRatioList"]
if len(preferenceModel) == len(preferenceRatioList):
    prefDict = dict(zip(preferenceModel, preferenceRatioList))
    pagesOfNews = list(mongoDB.getNews())
    newsClassList1 = [x['class'] for x in pagesOfNews]
    reorderedPagesOfNews = reorderPagesOfNews('a@b.com', pagesOfNews)
    newsClassList2 = [x['class'] for x in reorderedPagesOfNews]
    print "prefDict: --------------------------------------------"
    print prefDict
    print "newsClassList1: --------------------------------------"
    print newsClassList1
    print "newsClassList1: --------------------------------------"
    print newsClassList2
else:
    print "wrong size"