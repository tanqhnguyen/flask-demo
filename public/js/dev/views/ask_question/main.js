define([
  'marionette.custom'
  , 'models/question'
  , 'views/common/question_edit'
], function(Marionette, Question, QuestionEditView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      'click .js-submit': 'onSubmit'
    },

    initialize: function(options) {
      this.model = new Question({
        tags: []
      });
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    ui: {
      question: '.js-question'
    },

    onRender: function(){
      this.editView = new QuestionEditView({
        model: this.model,
        el: this.ui.question
      });
      this.editView.render();
    },

    onSubmit: function(e) {
      var $target = $(e.currentTarget);
      $target.bsbutton('loading');

      this.model.save().success(function(){

      }).complete(function(){
        $target.bsbutton('reset');
      });

    }
  });

  return View;
});