var path = require('path');
var express = require('express');
var app = express();

var index = require('./routes/index');

app.set('views', path.join(__dirname, '../client/build/'));  // TODO: how actually use this
app.set('view engine', 'jade'); // TODO: how actually use this
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));
app.use('/', index);

app.use(function(req, res) {
    // catch 404 and forward to error handler
    var err = new Error('Not Found');
    err.status = 404;
    res.send('404 Not Found');
});

module.exports = app;
