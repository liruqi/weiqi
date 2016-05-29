'use strict';

var gulp = require('gulp');
var util = require('gulp-util');
var browserify = require('browserify');
var vueify = require('vueify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sass = require('gulp-sass');
var karma = require('karma');

var config = {
    prod: !!util.env.production,
    js_main: './frontend/main.js',
    js_pattern: './frontend/**/*.js',
    scss_pattern: './frontend/css/**/*.scss',
    vue_pattern: './frontend/**/*.vue'
};

gulp.task('scripts', function() {
    var task = browserify({
        entries: config.js_main,
        debug: !config.prod
    })
        .transform('babelify', {presets: ['es2015']})
        .transform(vueify)
        .bundle()
        .pipe(source('all.js'))
        .pipe(config.prod ? buffer() : util.noop())
        .pipe(config.prod ? uglify() : util.noop())
        .pipe(gulp.dest('./static/dist'));
});

gulp.task('scripts:watch', function() {
    gulp.watch([config.vue_pattern, config.js_pattern], ['scripts']);
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
    new karma.Server({
        configFile: __dirname + '/karma.conf.js'
    }, done).start();
});

gulp.task('test', function(done) {
    var spawn = require('child_process').spawn;
    var cmd = spawn('py.test', ['-n8', 'weiqi'], {stdio: 'inherit'});
    
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

gulp.task('default', ['scripts', 'scripts:watch', 'sass', 'sass:watch', 'server', 'karma', 'fonts']);

gulp.task('build', ['scripts', 'sass', 'fonts']);
