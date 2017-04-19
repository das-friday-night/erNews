var router = require('express').Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res) {
    res.sendFile('index.html', {root: path.join(__dirname, '../../client/build')});
});

module.exports = router;


