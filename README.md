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


* To start either client or server by itself: `npm start`
* In script section of client/package.json. Except `npm start`, all other command need to do it with `run`, 
  for example: `npm run build` to build the react project.


**Remember to check out all the TODO questions**
