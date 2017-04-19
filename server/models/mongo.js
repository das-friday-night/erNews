const mongoose = require('mongoose');
const userModuel = require('./user');

module.exports.connect = (uri) => {
    mongoose.connect(uri);
    mongoose.connection.on('error', err => {
        console.error(`Mongoose Connection Error on Server: ${err}`);
        process.exit(1);
    });
};