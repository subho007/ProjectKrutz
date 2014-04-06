
/**
 * Module dependencies
 */

var express = require('express'),
  sqlite3 = require('sqlite3').verbose(),
  routes = require('./routes'),
  api = require('./routes/api'),
  http = require('http'),
  path = require('path');

var app = module.exports = express();

var file = '../Evolution of Android Applications.sqlite';
var db = new sqlite3.Database(file, sqlite3.OPEN_READONLY);


/**
 * Configuration
 */

// All environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.static(path.join(__dirname, 'public')));
app.use(app.router);

// Development only
if (app.get('env') === 'development') {
  app.use(express.errorHandler());
}

// Production only
if (app.get('env') === 'production') {
  // TODO
}


/**
 * Routes
 */

// Serve index and view partials
app.get('/', routes.index);
app.get('/partials/:name', routes.partials);

// JSON API
app.get('/api/rows', function (req, res) {
  db.all('SELECT * FROM ApkInformation', function (err, rows) {
    res.send(rows);
  });
});

// Redirect all others to the index (HTML5 history)
app.get('*', routes.index);


/**
 * Start Server
 */

http.createServer(app).listen(app.get('port'), function () {
  console.log('Express server listening on port ' + app.get('port'));
});
