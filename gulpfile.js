'use strict';

var gulp = require('gulp');
//var sourcemaps = require('gulp-sourcemaps');
var browserify = require('browserify');
var vueify = require('vueify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sass = require('gulp-sass');
var karma = require('karma');


gulp.task('scripts', function() {
    browserify({
        entries: './weiqi/frontend/main.js',
        debug: true
    })
        .transform('babelify', {presets: ['es2015']})
        .transform(vueify)
        .bundle()
        .pipe(source('all.js'))
        //.pipe(buffer())
        //.pipe(uglify())
        .pipe(gulp.dest('./weiqi/static/dist'));
});

gulp.task('sass', function() {
    return gulp.src('./weiqi/frontend/css/**/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('./weiqi/static/dist'))
});

gulp.task('scripts:watch', function() {
    gulp.watch(['./weiqi/frontend/**/*.vue', './weiqi/frontend/**/*.js'], ['scripts']);
});

gulp.task('sass:watch', function() {
    gulp.watch('./weiqi/frontend/css/**/*.scss', ['sass']);
});

gulp.task('server', function() {
    var spawn = require('child_process').spawn;
    spawn('python', ['-m', 'tornado.autoreload', 'main.py'], {stdio: 'inherit'})
});

gulp.task('testjs', function(done) {
    new karma.Server({
        configFile: __dirname + '/karma.conf.js'
    }, done).start();
});

gulp.task('default', ['scripts', 'scripts:watch', 'sass', 'sass:watch', 'server']);
