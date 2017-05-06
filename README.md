# erNews
## This is a journal of all the installation I did through out this project
## (Development use only)

1. (client) install [create-react-app](https://github.com/facebookincubator/create-react-app)
2. (client) install [materialize](http://materializecss.com/getting-started.html)
3. (server) install [express-generator](https://expressjs.com/en/starter/generator.html)
4. (server) install [nodemon](https://nodemon.io/)
5. (client) install [lodash](https://lodash.com/) : debounce
6. (backend-server) sudo intstall [python-jsonrpc](https://pypi.python.org/pypi/python-jsonrpc) : rpc server
7. (server) install [jayson](https://github.com/tedeh/jayson) : rpc client
8. install [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
9. (backend-server) install pymongo
10. (backend-server) install pika

11. (client) create client/src/Auth
12. (client) create client/src/Base
13. (client) create client/src/Login and client/src/SignUp
14. (client) install react-router@"<4.0.0" : version 4.0.0 has big change so that we use one version earlier
15. (client) we used configueration-styled router not component-styled router

16. (server) install cors
17. (server) install mongoose
18. (server) install bcrypt

19. (server) create schema and model for mongoose 
20. (server) config mongoDB connection

21. (server) install passport
22. (server) install passport-local: a passport strategy
23. (server) install jsonwebtoken
24. (server) create passport local strategies for login and signup
25. (server) create auth-checker middleware to guard route on '/news'
26. (server) initialize passport and setup auth-checker in app.js
27. (server) create route middleware auth.js to handle logic of '/auth'

28. (py-utils) install requests
29. (py-utils) install redis
30. (news-pipline) create news monitor
31. (news-pipline) install newspaper
    1. sudo apt-get install python-dev
    2. sudo apt-get install libxml2-dev libxslt-dev -y
    3. sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev -y
    4. sudo pip install newspaper
    5. curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python2.7
32. (news-pipline) create news scraper
33. (news-pipline) [install NumPy, SciPy, scikit-learn](http://scikit-learn.org/stable/install.html), dateutil
34. (news-pipline) create news deduper

35. (backend-server) create rpc server util to handle pagination, modify NewsPanel.js @ client, news.js routes and rpc-client.js @ server to handle pagination.

36. (recommend-service) create recommend_service: 
    - (client) NewsCard.js listen to click, restful post to node server
    - (server) add log transfer in news.js routes, call rpc-client logNewsClick
    - (backend-server) rpc-server call rpc-server-util and send log rpc request to rabbitmq
    - click log processor receive rabbitmq, handle time decay model by click
    - create a new rpc server: recommend-server at port 5050 
    - create a new rpc client: recommend-client in py-util
    - recommend-client expose service for other user to get a user's preference model

37. install jupyter via dockerfile
    - sudo docker build . -t siyuanli/cs503_tensorflow_jupyter
    - sudo docker login
    - sudo docker push siyuanli/cs503_tensorflow_jupyter

38. run jupyter
    - docker run -it --rm -p 8888:8888 siyuanli/cs503_tensorflow_jupyter

39. upload tensorflow.ipynb, go through the tutorial to learn tensorflow
40. create news classifier service
    - install tensorflow and pandas
    - create news cnn model to setup convolution steps, one hot word processing, loss function, training process
    - create classifier trainer to setup vocabulary processor, estimator, fit, prediction and accuracy calculation
    - import all news training and testing data in labeled_news.csv
41. expose the news classifier service as a rpc server
    - create function to load trained model and vocabulary processor
    - install [watchdog](https://pythonhosted.org/watchdog/) to monitor cnn model change. working as a hot starter, meaning that once new training model updated, this watchdog could update the current loaded trained model and vocabulary processor correspondingly. Notice that once model and vocabulary processor are trained with new data, the state(information) in the classifier object and the vocab_processor object are still using the outdated state. Hence, manual update needed
42. create a classifier service rpc client in py_utils
43. update news_scraper with classifier function before store a new news into database


* To start either client or server by itself: `npm start`
* In script section of client/package.json. Except `npm start`, all other command need to do it with `run`, 
  for example: `npm run build` to build the react project.
* All python file or folder should be named in _ style but NOT - style. Since the import not work with - 


**Remember to check out all the TODO questions**
