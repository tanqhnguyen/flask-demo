var path = require('path');
var fs = require('fs');

var modules = [
  'home',
  'topics',
  'view_article',
  'submit_article',
  'view_topic',
  'create_topic',
  'search',
  'tags',
  'approve_article'
];

var requireOptions = require('../js/build.json')
requireOptions['baseUrl'] = path.join(__dirname, '..', 'js', 'dev');
requireOptions['dir'] = path.join(__dirname, '..', 'js', 'production');
requireOptions['preserveLicenseComments'] = false;
//requireOptions['optimize'] = 'none';

var lessFiles = {};
for (var i in modules) {
  var less = ['..', 'less', modules[i]+'.less'].join('/');
  var css = ['..', 'css', modules[i]+'.css'].join('/');
  lessFiles[css] = less;
}

module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-less');

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    requirejs: {
      app: {
        options: requireOptions
      }
    },

    less: {
      app: {
        options: {
          compress: true,
          cleancss: true,
          paths: [
            path.join('..', 'less')
          ]
        },
        files: lessFiles
      }
    }
  });

  grunt.registerTask('build', ['requirejs:app', 'less:app']);

}
