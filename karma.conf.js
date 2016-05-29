module.exports = function(config) {
    config.set({
        browsers: ['PhantomJS'],

        frameworks: ['browserify', 'mocha'],

        files: [
            'frontend/**/*_test.js'
        ],

        preprocessors: {
            'frontend/**/*_test.js': ['browserify']
        },

        browserify: {
            debug: true,
            transform: [['babelify', {'presets': 'es2015'}], 'vueify']
        }
    });
};
