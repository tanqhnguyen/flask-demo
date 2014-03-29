define([
  'backbone.custom'
  , 'marionette.custom'
  , 'views/common/question'
  , 'forms/answer_edit'
  , 'models/answer'
  , 'views/view_question/answer'
  , 'views/common/load_more'
], function(Backbone, Marionette, QuestionView, AnswerForm, Answer, AnswerView, LoadMoreView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      'click .js-send': 'onSend',
      'click .js-refresh': 'onClickRefresh'
    },

    ui: {
      question: '.js-question',
      answerForm: '.js-answer-form',
      answerList: '.js-answer-list'
    },

    initialize: function() {
      var self = this;
      this.answer = new Answer();
      this.answer.set('question_id', this.model.id);

      this.answerForm = new AnswerForm({
        model: this.answer
      });

      this.answersView = new LoadMoreView({
        model: this.model,
        collection: this.model.get('answers'),
        el: this.ui.answerList,
        itemView: AnswerView,
        modelData: {
          'question_id': 'id'
        }
      });

      this.listenTo(this.answersView, 'fetch', function(response){
        self.model.set('answer_count', response.pagination.total);
      });

      this.questionView = new QuestionView({
        model: this.model,
        el: this.ui.question
      });
    },

    onRender: function(){
      this.questionView.render();

      this.answerForm.buildControl('content', this.ui.answerForm, {

      });

      this.answersView.render();
    },

    onSend: function(e) {
      var self = this;

      var $currentTarget = $(e.currentTarget);
      $currentTarget.bsbutton('loading');

      this.answer.save().complete(function(){
        $currentTarget.bsbutton('reset');
      }).success(function(){
        self.answerForm.getControl('content').markdownEditor.setValue('');
        self.answer.id = void 0;
        self.onClickRefresh();
      })
    },

    onClickRefresh: function(e) {
      this.answersView.triggerMethod('refresh');
    }
  });

  return View;
});