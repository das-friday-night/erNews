const PassportLocalStrategy = require('passport-local').Strategy;
const User = require('mongoose').model('users');
const jwt = require('jsonwebtoken');
const yaml = require('js-yaml');
const fs = require('fs');
const config = yaml.safeLoad(fs.readFileSync('../../../config.yaml', 'utf8'));

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

    User.findOne({email : userData.email}, (err, user) => {
        if(err) return done(err);

        // check if user info can be found via email
        if(!user) {
            const error = new Error('email not existed');
            error.name = 'IncorrectCredentialsError';
            return done(error);
        }

        // check if input email and password match with database data
        return user.comparePassword(userData.password, (err, isMatch)=>{
            if(err) return done(err);

            if(!isMatch) {
                const error = new Error('Incorrect email or password');
                error.name = 'IncorrectCredentialsError';
                return done(error);
            }

            const payload = {sub: user._id};
            const token = jwt.sign(payload, config['JWT_SECRET']);
            const data = {name: user.email};
            // data: for the client to know token corresponding to which user
            return done(null, token, data);
        });
    });
});