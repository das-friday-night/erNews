## This doc is a breif of [official tutorial](http://passportjs.org/docs/overview)

# In short, Passport is authentication middleware for Node

## Server
### Three thing to configue Passport
    1. Authentication strategies (e.g. passport-local)
    2. Application middleware
    3. Sessions (optional)

### 1: strategies
By default, LocalStrategy expects to find credentials in parameters named `username` and `password`
```javascript
var passport = require('passport')
  , LocalStrategy = require('passport-local').Strategy;

passport.use(new LocalStrategy(
  function(username, password, done) {
    User.findOne({ username: username }, function(err, user) {
      if (err) { return done(err); }
      if (!user) {
        return done(null, false, { message: 'Incorrect username.' });
      }
      if (!user.validPassword(password)) {
        return done(null, false, { message: 'Incorrect password.' });
      }
      // see comment below about done
      return done(null, user);
    });
  }
));
```
`done`: named verify callback. 
* If the credentials are valid, the verify callback invokes `done` to supply Passport with the user that authenticated.
`return done(null, user);`
* If the credentials are not valid (for example, if the password is incorrect), done should be invoked with false instead of a user to indicate an authentication failure.
`return done(null, false);`
* An additional info message can be supplied to indicate the reason for the failure. 
`return done(null, false, { message: 'Incorrect password.' });`
* if an exception occurred while verifying the credentials (for example, if the database is not available), done should be invoked with an error, in conventional Node style.
`return done(err);`

If your site prefers to name these fields differently, options are available to change the defaults.
```javascript
passport.use(new LocalStrategy({
    usernameField: 'email',
    passwordField: 'passwd'
  },
  function(username, password, done) {
    // ...
  }
));
```

### 2: middleware
#### 1. Initialization
* passport.initialize() middleware is required to initialize Passport
* application uses persistent login sessions, passport.session() middleware must also be used.
```javascript
app.configure(function() {
  app.use(express.static('public'));
  app.use(express.cookieParser());
  app.use(express.bodyParser());
  app.use(express.session({ secret: 'keyboard cat' }));
  app.use(passport.initialize());
  app.use(passport.session());
  app.use(app.router);
});
```

#### 2. Authenticate at certain route
Most simple way: 
```javascript
app.post('/login', passport.authenticate('local', { successRedirect: '/',
                                                    failureRedirect: '/login' }));
```
Another way: 
```javascript
app.post('/login',
  passport.authenticate('local'),
  function(req, res) {
    // If this function gets called, authentication was successful.
    // `req.user` contains the authenticated user.
    res.redirect('/users/' + req.user.username);
  });
```
Custom way:
```javascript
app.get('/login', function(req, res, next) {
  passport.authenticate('local', function(err, user, info) {
    if (err) { return next(err); }
    if (!user) { return res.redirect('/login'); }
    req.logIn(user, function(err) {
      if (err) { return next(err); }
      return res.redirect('/users/' + user.username);
    });
  })(req, res, next);
});
```

### 3: sessions
If authentication succeeds, a session can be used on subsequent request. But rather the unique cookie that identifies the session. In order to support login sessions, Passport will serialize and deserialize user instances to and from the session.
```javascript
passport.serializeUser(function(user, done) {
  done(null, user.id);
});

passport.deserializeUser(function(id, done) {
  User.findById(id, function(err, user) {
    done(err, user);
  });
});
```

session support can be safely disabled by setting the session option to false.
```javascript
app.get('/api/users/me',
  passport.authenticate('basic', { session: false }),
  function(req, res) {
    res.json({ id: req.user.id, username: req.user.username });
  });

```
