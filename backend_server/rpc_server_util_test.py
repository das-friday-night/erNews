from rpc_server_util import getNews
from sets import Set

page1 = getNews('XiaoWang', 0)
page2 = getNews('XiaoWang', 1)

print 'page1: %i' % len(page1)
print 'page2: %i' % len(page2)

page_1_set = Set([news['digest'] for news in page1])
page_2_set = Set([news['digest'] for news in page2])

assert len(page_1_set.intersection(page_2_set)) == 0

print 'test pass'