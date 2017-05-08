var jayson = require('jayson');
var yaml = require('js-yaml');
var fs = require('fs');
var path = require('path');

// create a client
var config = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../../config.yaml'),'utf8'));
var client = jayson.client.http({
  port: config['RPC_SERVER']['PORT'],
  hostname: config['RPC_SERVER']['HOST']
});

// a test function
function add(a, b, callback){
    client.request('add', [a, b], function(err, response) {
        if(err) throw err;
        console.log(response);
        callback(response.result);
    });
}

function getNews(userID, pageID, callback){
    client.request('getNews', [userID, pageID], function(err, response) {
        if(err) throw err;
        callback(response.result);
    });
}

function logNewsClick(userID, newsID){
    client.request('logNewsClick', [userID, newsID], function(err, response){
        if(err) throw err;
        console.log(response);
    });
}

module.exports = {
    add : add,
    getNews : getNews,
    logNewsClick : logNewsClick
}

