var client = require('./rpc-client');

client.add(1,1,function(res){
    console.assert(res == 2);
});