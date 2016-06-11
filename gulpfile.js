'use strict';

var gulp = require('gulp');
var util = require('gulp-util');
var webpack = require('webpack');
var sass = require('gulp-sass');
var karma = require('karma');

if(util.env.production) {
    process.env.NODE_ENV = 'production';
}

var config = {
    prod: !!util.env.production,
    scss_pattern: './frontend/css/**/*.scss',
};

var webpack_config = require('./webpack.config.js');

if(!util.env.production) {
    webpack_config.watch = true;
}

gulp.task('scripts', function() {
    webpack(webpack_config, function(error, stats) {
        if (error) {
            util.log('[webpack]', error);
        }

        util.log('[webpack]', stats.toString({
            colors: true, hash: false, version: false, timings: false, assets: true, chunks: false,
            chunkModules: false, modules: false, children: false, cached: false, reasons: false,
            source: false, errorDetails: false, chunkOrigins: false
            //context: '', modulesSort: '', chunksSort: '', assetsSort: ''
        }));
    });
});

gulp.task('sass', function() {
    return gulp.src(config.scss_pattern)
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(gulp.dest('./static/dist'))
});

gulp.task('sass:watch', function() {
    gulp.watch(config.scss_pattern, ['sass']);
});

gulp.task('server', function() {
    var spawn = require('child_process').spawn;
    spawn('python', ['-m', 'tornado.autoreload', 'main.py'], {stdio: 'inherit'});
});

gulp.task('karma', function(done) {
    // Does not work with current webpack configuration
    /*new karma.Server({
        configFile: __dirname + '/karma.conf.js'
    }, done).start();*/
});

gulp.task('test', function(done) {
    var spawn = require('child_process').spawn;
    var cmd = spawn('py.test', ['-n8', '--benchmark-skip', 'weiqi'], {stdio: 'inherit'});
    
    cmd.on('close', function() {
        new karma.Server({
            configFile: __dirname + '/karma.conf.js',
            singleRun: true
        }, done).start();
    });
});

gulp.task('fonts', function() {
  return gulp.src('node_modules/font-awesome/fonts/*')
    .pipe(gulp.dest('./static/dist/fonts'))
});

gulp.task('default', ['scripts', 'sass', 'sass:watch', 'server', 'karma', 'fonts']);

gulp.task('build', ['scripts', 'sass', 'fonts']);
