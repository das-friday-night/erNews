import requests
from json import loads
from config import NEWSAPI

def getNewsFromNewsAPI(sources=NEWSAPI['DEFAULT_SOURCES'], sort=NEWSAPI['DEFUALT_SORT']):
    articles = []

    for source in sources:
        payload = {
            'source': source,
            'sortBy': sort,
            'apiKey': NEWSAPI['KEY']
        }

        response = requests.get(NEWSAPI['API_BASE'], params=payload)
        if(response.status_code != 200): 
            print "Error in newsapi request"
            return articles

        response = loads(response.content)

        if (response is not None and 
        response['status'] == 'ok' and 
        response['source'] is not None):

            # add source to each news to be used in news handling
            for news in response['articles']:
                news['source'] = response['source']

            # append news to return variable.
            articles.extend(response['articles'])
            
    return articles
