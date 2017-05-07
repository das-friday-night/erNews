from newsapi_client import getNewsFromNewsAPI

def test_basic():
    # news = getNewsFromNewsAPI()
    # print news
    # assert len(news) > 0
    news = getNewsFromNewsAPI(sources=['bbc-news'])
    assert len(news) > 0
    print 'test_basic passed!'

if __name__ == "__main__" :
    test_basic()