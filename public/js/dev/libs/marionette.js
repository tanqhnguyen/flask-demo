define([
  'underscore.custom'
  , 'vendors/backbone.marionette'
  , 'models/current_user'
], function(_, Marionette, currentUser){
  window.currentUser = currentUser;

  _.extend(Marionette.View.prototype, {
    runOnce: function(fn, delay) {
      var self = this;
      clearTimeout(this.$el.data(this.cid));
      this.$el.data(this.cid, setTimeout(function(){
        fn.apply(self);
      }, delay));
    },

    getOption: function(name) {
      return Marionette.getOption(this, name);
    }
  });

  return Marionette;
});