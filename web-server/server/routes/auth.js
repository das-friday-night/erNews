const express = require('express');
const router = express.Router();
const validator = require('validator');
const passport = require('passport');

router.post('/signup', (req, res, next) => {
    const validationResult = validatesSignupForm(req.body);
    if(!validationResult.success){
        console.log('validation failed');
        return res.status(400).json({
            success: false,
            message: validationResult.message,
            errors: validationResult.errors
        });
    }

    return passport.authenticate('local-signup', err=>{
        if(err){
            console.log(err);
            if(err.name === 'MongoError' && err.code === 11000){
                // the 11000 Mongo code is for a duplication email error
                // the 409 HTTP status code is for conflict error
                return res.status(409).json({
                    success: false,
                    message: 'duplicate email error.',
                    errors: {
                        email: 'This email is already taken.'
                    }
                });
            }

            return res.status(400).json({
                success: false,
                message: "can't process form" 
            });
        }

        return res.status(200).json({
            success: true,
            message: 'signup successful. Please login Now.'
        });
    })(req, res, next);
});


router.post('/login', (req, res, next) => {
    const validationResult = validatesLoginForm(req.body);
    if(!validationResult.success){
        console.log('validation failed');
        return res.status(400).json({
            success: false,
            message: validationResult.message,
            errors: validationResult.errors
        });
    }

    return passport.authenticate('local-login', (err, token, data) =>{
        if(err){
            console.log(err);
            if(err.name === 'IncorrectCredentialsError'){
                return res.status(400).json({
                    success: false,
                    message: err.message
                });
            }
        }

        return res.status(200).json({
            success: true,
            message: 'login successful.',
            token,
            user: data
        });
    })(req, res, next);
});

function validatesSignupForm(payload){
    const errors = {};
    let isFormValid = true;
    let message = '';

    // this is used for email and password sanity check
    if(!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)) {
        isFormValid = false;
        errors.email = 'Please provide a correct email address.';
    }

    if(!payload || typeof payload.password !== 'string' || payload.password.trim().length < 8) {
        isFormValid = false;
        errors.password = 'Password must have at least 8 characters.';
    }

    if(!isFormValid) {
        message = 'Check the form for errors.';
    }

    // TODO: message dont need to write like message: message?
    return {
        success: isFormValid,
        message,
        errors
    };
}

function validatesLoginForm(payload){
    const errors = {};
    let isFormValid = true;
    let message = '';

    if(!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0){
        isFormValid = false;
        errors.email = 'Please provide a email address.';
    } 

    if(!payload || typeof payload.password !== 'string' || payload.password.trim().length === 0){
        isFormValid = false;
        errors.password = 'Please provide a password.';
    } 
    if(!isFormValid){
        message = 'Check the form for errors';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

module.exports = router;