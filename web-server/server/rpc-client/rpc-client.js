var jayson = require('jayson');

// create a client
var client = jayson.client.http({
  port: 4040,
  hostname: 'localhost'
});

// invoke "add"
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

module.exports = {
    add : add,
    getNews : getNews
}

