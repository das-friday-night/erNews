var path = require('path');
var express = require('express');
var app = express();

var index = require('./routes/index');
var news = require('./routes/news');

app.set('views', path.join(__dirname, '../client/build/'));  // TODO: how actually use this
app.set('view engine', 'jade'); // TODO: how actually use this

// TODO: for purpose of developing client and server at same time, delete after client finished developement
app.all('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type");
    next();
});

app.use('/static', express.static(path.join(__dirname, '../client/build/static')));
app.use('/news/', news);
app.use('/', index);

app.use(function(req, res) {
    // catch 404 and forward to error handler
    var err = new Error('Not Found');
    err.status = 404;
    res.status(404).send('404 Not Found');
});

module.exports = app;
