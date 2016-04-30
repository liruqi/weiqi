module.exports = function(config) {
    config.set({
        browsers: ['PhantomJS'],

        frameworks: ['browserify', 'jasmine'],

        files: [
            'weiqi/frontend/**/*_test.js'
        ],

        preprocessors: {
            'weiqi/frontend/**/*_test.js': ['browserify']
        },

        browserify: {
            debug: true,
            transform: [['babelify', {'presets': 'es2015'}], 'vueify']
        }
    });
};
