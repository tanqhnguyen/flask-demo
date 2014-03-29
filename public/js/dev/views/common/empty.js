define([
  'underscore.custom'
  , 'marionette.custom'
  , 'text!templates/common/empty.html'
], function(_, Marionette, empty){
  return Marionette.ItemView.extend({
    template: function() {
      return _.template(empty, {
        random: _.random(0,3)
      });
    }
  })
})