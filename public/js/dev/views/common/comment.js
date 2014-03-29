define([
  'marionette.custom'
], function(Marionette){

  var ItemView = Marionette.ItemView.extend({
    template: '#comment-template',

    className: 'comment',

    events: {
      'click .js-delete': 'onClickDelete',
      'click .js-block': 'onClickBlock'
    },

    ui: {
      content: '.js-content'
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    initialize: function(options) {

    },

    onRender: function() {
      
    },

    onClickDelete: function() {
      this.model.destroy();
    },

    onClickBlock: function() {
      this.model.get('user').ban();
    }
  });

  return ItemView;

});