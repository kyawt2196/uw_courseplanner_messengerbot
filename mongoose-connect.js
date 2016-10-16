var mongoose = require('mongoose');
var config = require('./config.js');

module.exports.connect = 
    // Returns a reference to the mongoose db:
    (app) => {
        switch(app.get('env')) {
            case 'development':
                mongoose.connect('mongodb://straw:berry@ds031965.mlab.com:31965/mixfruitdb', config.mongooseOpts);
                break;
            case 'production':
                mongoose.connect('mongodb://straw:berry@ds031965.mlab.com:31965/mixfruitdb', config.mongooseOpts);
                break;
            default:
                throw new Error('Unknown execution enviroment for MongoDB: ' + app.get('env'));
        }
    };