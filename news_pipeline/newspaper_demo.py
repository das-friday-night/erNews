# -*- coding: utf-8 -*-
from newspaper import Article

# this will cause an error

article = Article('http://www.businessinsider.com/warren-buffett-at-berkshire-meeting-on-ahca-obamacare-gop-healthcare-2017-5')
article.download()
try: 
    article.parse()
except ValueError:
    print len(article.text)