define([
  'marionette.custom'
  , 'libs/rivets'
], function(Marionette, rivets){

  var ItemView = Marionette.ItemView.extend({
    template: '#topic-template',

    className: 'topic',

    events: {

    },

    initialize: function() {

    },

    ui: {
      tags: '.js-tags'
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    onRender: function() {
      var self = this;
      rivets.bind(this.$el, {
        model: this.model
      });
    }
  });

  return ItemView;
});