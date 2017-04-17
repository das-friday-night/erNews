const PassportLocalStrategy = require('passport-local').Strategy;
const User = require('../models/user');

// strategy is seperate from passport.authenticate. a way to decoupling
module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
},(req, email, password, done) =>{
    const userData = {
        email: email.trim(),
        password: password.trim()
    };
    const newPotentialUser = User(userData);
    
    // newPotentialUser: we don't know if this user saved already
    // duplication check will be handle by pre-save hook defined in user.js

    newPotentialUser.save(err => {
        if(err) {
            console.log("Error in saving signup data to mongo");
            console.log(err);
            return done(err);
        }
        console.log('New user saved in user database');
        return done(null);
    });

});