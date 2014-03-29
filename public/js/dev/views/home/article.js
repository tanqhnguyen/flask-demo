define([
  'marionette.custom'
  , 'libs/rivets'
], function(Marionette, rivets){

  var ItemView = Marionette.ItemView.extend({
    template: '#article-template',

    className: 'article preview',

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