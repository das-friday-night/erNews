const jwt = require('jsonwebtoken');
const config = require('../config/config.json');
const User = require('../models/user');

module.exports = (req, res, next) => {
    //TODO: header authorization is set where?
    if(!req.headers.authorization) return res.status(401).end();

    // get the last part from a authorization header string like "bearer token-value"
    const token = req.headers.authorization.split(' ')[1];

    // decode the token using a secret key-phrase
    return jwt.verify(token, config['jwtSecret'], (err, decoded)=>{
        // the 401 code is for unauthorized status
        if(err)  return res.status(401).end(); 

        const email = decoded.sub;
        return User.findById(email, (err, user)=>{
            if(err || !user) return res.status(401).end();
            return next();
        });
    });
}; 