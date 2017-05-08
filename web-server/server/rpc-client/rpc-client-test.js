// to start this test, do: 
// $ node rpc-client-test.js

var client = require('./rpc-client');


// client.getNews('XiaoWang',0,function(res){
//     console.log(res.length);
//     console.log(Array.isArray(res));
// });

client.add(2,3, function(res){
    console.log(res)
});