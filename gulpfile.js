'use strict';
var gulp,
    sass,
    merge,
    concat,
    shell;

//load dependencies
gulp = require('gulp');
sass = require('gulp-sass');
merge = require('merge-stream');
concat = require('gulp-concat');
shell = require('gulp-shell')

//define default task
gulp.task('sass', function () {
    var sassStream,
        cssStream;

    //select additional css files
    cssStream = gulp.src(['./app/static/stylesheets/*.css']);

    //compile sass
    sassStream = gulp.src('./app/static/stylesheets/**/*.scss')
        .pipe(sass({
            errLogToConsole: true
        }));

    //merge the two streams and concatenate their contents into a single file
    return merge(sassStream, cssStream)
        .pipe(concat('theapp.css'))
        .pipe(gulp.dest('./app/static/stylesheets/'))
        .pipe(shell(['python manage.py collectstatic --noinput']));
});

gulp.task('default', ['sass']);
