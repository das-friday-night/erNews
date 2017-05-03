var router = require('express').Router();
var rpcClient = require('../rpc-client/rpc-client');

router.get('/userId/:userId/pageID/:pageID', function(req, res) {
    let userID = req.params['userId'];
    let pageID = req.params['pageID'];
    rpcClient.getNews(userID, pageID, function(newsList){
        res.json({ news: newsList});
    });
});

router.post('/userId/:userId/newsID/:newsID', function(req, res) {
    let userID = req.params['userId'];
    let newsID = req.params['newsID'];
    rpcClient.logNewsClick(userID, newsID);
    res.status(200);
});

module.exports = router;
