var
 express  = require('express'),
 fs      = require('fs'),
 exec    = require('exec'),
 passport = require('passport'),
 BearerStrategy = require('passport-http-bearer').Strategy,
// uuid = require('node-uuid'),

 app = express();
// *************************************************************
// USER
// *************************************************************
var users = [
    { id: 1, username: 'user', token: 'pw', email: 'sandro@scalco.ch' }
];

function findByToken(token, fn) {
  for (var i = 0, len = users.length; i < len; i++) {
    var user = users[i];
    if (user.token === token) {
      return fn(null, user);
    }
  }
  return fn(null, null);
}


// *************************************************************
// USE
// *************************************************************
// https://github.com/jaredhanson/passport-http-bearer/blob/master/examples/bearer/app.js

passport.use(new BearerStrategy({
  },
  function(token, done) {
    // asynchronous validation, for effect...
    process.nextTick(function () {

      // Find the user by token.  If there is no user with the given token, set
      // the user to `false` to indicate failure.  Otherwise, return the
      // authenticated `user`.  Note that in a production-ready application, one
      // would want to validate the token for authenticity.
      findByToken(token, function(err, user) {
        if (err) {
         console.log("Error TOken not found");
         return done(err);
        }
        if (!user) {
         console.log("no user found");
         return done(null, false);
        }
        console.log("Login mit User: " + user.username );
        return done(null, user);

      })
    });
  }
));

//app.use(express.logger());
  // Initialize Passport!  Note: no need to use session middleware when each
  // request carries authentication credentials, as is the case with HTTP
  // Bearer.
app.use(passport.initialize());
 //app.use(app.router);
 //app.use(express.static(__dirname + '/public'));

// *************************************************************
// GET
// Authenticate using HTTP Bearer credentials,
// with session support disabled.
// *************************************************************
app.get('/wohnzimmer/temp',
 passport.authenticate('bearer', { session: false }),
 function(req, res){
  console.log("GET / readings.py");
//  var python = require('child_process').spawn('python',"/home/pi/readings.py");

//  python.on('close', function(code){
 //   console.log("python close ");
 //   if (code !== 0) {
//      console.log("error");
//      return res.status(500).send("error, temp lesen via script");
//    }
    console.log("lesen der wetterdaten beginnen");
    fs.readFile('wetterdaten.json', 'utf8', function (err, data) {
      //if (err) throw err;
      console.log("daten erfolgreich gelesen " + data);
      res.jsonp(JSON.stringify({ temperatur: data }, null, 3));
    });
//  }); //python close
});       //get

app.get('/wetterdaten/ch',
 passport.authenticate('bearer', { session: false }),
 function(req, res){

//  var python1 = require('child_process').spawn('python',"/home/pi/opendata.py");

//  python1.on('close', function(code){
//    console.log("close python");
//    if (code !== 0) {
//      console.log("error");
//      return res.status(500).send("error, tempdaten schweiz lesen via script");
//    }
    console.log("Start lesen wertterdateschweiz");
    fs.readFile('wetterdaten_schweiz.json', 'utf8', function (err, data) {
      //if (err) throw err;
      console.log("daten erfolgreich gelesen");
      res.jsonp(JSON.stringify(data, null, 3));
    });
//  }); //python close
});       //get

app.get('/camera',
 passport.authenticate('bearer', { session: false }),
 function(req, res){
  console.log('GET /Camera');

  exec('/home/pi/camera/camera.sh',
   function (error, stdout, stderr) {
//    console.log('stdout: ' + stdout);
//    console.log('stderr: ' + stderr);

   var filename = stdout.replace(/(\r\n|\n|\r)/gm," ").trim();

   console.log('Filename direkt aus stdout: ' + stdout );

   fs.readFile(filename, function(err, data) {
//     if (err) throw err; // Fail if the file can't be read

   res.jsonp(JSON.stringify({ image: new Buffer(data).toString('base64') }, null, 3));

// ATTACH JPG to response.
//    res.writeHead(200, {'Content-Type': 'image/jpg'});
//    res.end(data); // Send the file data to the browser.


// ATTACH HTML Site to response
//     res.writeHead(200, {'Content-Type': 'text/html'});
//    res.write('<html><body><h1>Wetterstation</h1><img src="data:image/jpeg;base64,')
//     res.write(new Buffer(data).toString('base64'));
//     res.end('"/></body></html>');
   });

  }); // process

});//get camera

app.listen(3000, function(){
console.log("server running");
});
