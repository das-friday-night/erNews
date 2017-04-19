from newsapi_client import getNewsFromNewsAPI

def test_basic():
    news = getNewsFromSource()
    print news
    assert len(news) > 0
    news = getNewsFromSource(sources=['bbc-news'])
    assert len(news) > 0
    print 'test_basic passed!'

if __name__ == "__main__" :
    test_basic()