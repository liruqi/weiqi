var webpack_config = require('./webpack.config.js');

webpack_config.plugins = [];
webpack_config.entry = "";

module.exports = function(config) {
    config.set({
        browsers: ['PhantomJS'],

        frameworks: ['mocha'],

        files: [
            'frontend/**/*_test.js'
        ],

        preprocessors: {
            'frontend/**/*_test.js': ['webpack']
        },
        
        webpack: webpack_config,
        
        webpackMiddleware: {
            noInfo: true,
            quiet: true,
        }
    });
};
