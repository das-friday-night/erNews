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

UserSchema.methods.comparePassword = function (password, callback){
    bcrypt.compare(password, this.password, callback);
};

// info about mongoose middleware
// http://mongoosejs.com/docs/middleware.html
UserSchema.pre('save', function(next) {
    // TODO: dont understand why do this
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