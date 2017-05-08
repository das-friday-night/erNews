var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var mongoose = require('mongoose');
var passport = require('passport');
var path = require('path');
var yaml = require('js-yaml');
var fs = require('fs');

var index = require('./routes/index');
var news = require('./routes/news');
var auth = require('./routes/auth');

var app = express();

// connect mongoDB to store username and password
var config = yaml.safeLoad(fs.readFileSync('../../config.yaml','utf8'));
require('./models/mongo').connect(config['MONGO']['URI']);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));  // TODO: how actually use this
app.set('view engine', 'jade'); // TODO: how actually use this
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));

// TODO: for purpose of developing client and server at same time, delete after client finished developement
app.use(cors());
app.use(bodyParser.json());

// load passport strategies
app.use(passport.initialize());
var signUpStrategy = require('./passport/signup-strategy');
var loginStrategy = require('./passport/login-strategy');
passport.use('local-signup', signUpStrategy);
passport.use('local-login', loginStrategy);

// pass the authenticaion checker middleware
var authCheckMiddleware = require('./middleware/auth-checker');
app.use('/news', authCheckMiddleware);

app.use('/', index);
app.use('/news', news);
app.use('/auth', auth);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    res.status(404).send('404 Not Found');
});

module.exports = app;
