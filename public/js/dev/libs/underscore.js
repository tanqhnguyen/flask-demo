define([
  'underscore'
  , 'vendors/underscore.string'
], function(_, _s, arrg){
  _.mixin(_s);

  _.mixin({
    t: function(lookup, data) {
      return window.appData.translations[lookup] || lookup;
    },

    stackTrace: function() {
      var e = new Error('dummy');
            var stack = e.stack.replace(/^[^\(]+?[\n$]/gm, '')
                .replace(/^\s+at\s+/gm, '')
                .replace(/^Object.<anonymous>\s*\(/gm, '{anonymous}()@')
                .split('\n');
            console.log(stack);
    },

    hasPermission: function(name) {
      return window.currentUser.hasPermission(name);
    }
  });

  return _;
});