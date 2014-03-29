define([
  'marionette.custom'
  , 'views/common/question'
  , 'views/common/load_more'
], function(Marionette, QuestionView, LoadMoreView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      
    },

    ui: {
      questions: '.js-questions'
    },

    initialize: function() {
      
    },

    onRender: function(){
      this.articlesView = new LoadMoreView({
        collection: this.collection,
        el: this.ui.questions,
        itemView: QuestionView
      });
      this.articlesView.render();
    }
  });

  return View;
});