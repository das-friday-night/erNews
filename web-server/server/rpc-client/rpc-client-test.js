// to start this test, do: 
// $ node rpc-client-test.js

var client = require('./rpc-client');

client.add(1,1,function(res){
    console.assert(res == 2);
});

client.getNews();