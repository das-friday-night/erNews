const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// TODO: learn index in mongo
// https://docs.mongodb.com/manual/indexes/
const UserSchema = mongoose.Schema({
    email: {
        type: String,
        index: { unique: true }
    },
    password: String
});

// *** Reason to use "function" instead of arrow function:
// this method will be called by a mongo document object at runtime. 
// arrow function will cause "this" point to "undefined", while
// "function" will be treated as a method invocation and "this" will 
// be the object that owns the method which is the mongo document object
UserSchema.methods.comparePassword =  function (password, callback) {
    bcrypt.compare(password, this.password, callback);
};

// info about mongoose middleware
// http://mongoosejs.com/docs/middleware.html
// use "function" in purpose: see ***
UserSchema.pre('save', function(next) {
    // To add readablity assign this to user. since this in the runtime context
    // is the user document.
    const user = this;

    // return next: https://stackoverflow.com/questions/33629897/return-next-in-nodejs-confusion
    // proceed further only if the password is modified or the user is var new
    if(!user.isModified('password')) return next();
    
    return bcrypt.genSalt((saltError, salt)=>{
        if(saltError) {
            console.log("Error when generate salt");
            console.log(saltError);
            return next(saltError);
        }
        
        return bcrypt.hash(user.password, salt, (hashError, hash) =>{
            if (hashError) {
                console.log("Error when generate hash");
                console.log(hashError);
                return next(hashError);
            }

            user.password = hash;
            return next();
        });
    });
});

// 'users' is the collection name
module.exports = mongoose.model('users', UserSchema);