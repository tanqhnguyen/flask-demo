define([
  'marionette.custom'
  , 'forms/answer_display'
], function(Marionette, AnswerForm){

  var ItemView = Marionette.ItemView.extend({
    template: '#answer-template',

    className: 'answer',

    ui: {
      content: '.js-content'
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    initialize: function(options) {
      this.form = new AnswerForm({
        model: this.model
      });
    },

    onRender: function() {
      this.form.buildControl('content', this.ui.content);
    }
  });

  return ItemView;

});