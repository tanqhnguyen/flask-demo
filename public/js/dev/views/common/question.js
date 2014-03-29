define([
  'marionette.custom'
  , 'forms/question_display'
  , 'forms/comment_edit'
  , 'models/comment'
], function(Marionette, QuestionForm, CommentForm, Comment){

  var ItemView = Marionette.ItemView.extend({
    template: '#question-template',

    className: 'question preview',

    events: {
      'click .js-vote-up': 'onVoteUp',
      'click .js-vote-down': 'onVoteDown',
      'click .js-show-comment-form': 'onClickShowCommentForm',
      'click .js-send-comment': 'onSend'
    },

    initialize: function() {
      this.form = new QuestionForm({
        model: this.model
      });

      this.comment = new Comment({
        question_id: this.model.id
      });

      this.commentForm = new CommentForm({
        model: this.comment
      });
    },

    ui: {
      tags: '.js-tags',
      title: '.js-title',
      content: '.js-content',
      author: '.js-author',
      sidebar: '.js-sidebar',
      votePoints: '.js-vote-points',
      voteUp: '.js-vote-up',
      voteDown: '.js-vote-down',
      answerCount: '.js-answer-count',
      commentList: '.js-comment-list',
      commentForm: '.js-comment-form',
      sendComment: '.js-send-comment'
    },

    serializeData: function() {
      return {
        model: this.model,
        form: this.form
      };
    },

    onRender: function() {
      var self = this;
      this.form.buildControl('title', this.ui.title);
      this.form.buildControl('content', this.ui.content);
      this.form.buildControl('user.name', this.ui.author);
      this.form.buildControl('tags', this.ui.tags);
      this.form.buildControl('points', this.ui.votePoints);
      this.form.buildControl('answer_count', this.ui.answerCount);
    },

    onVoteUp: function(e) {
      var $currentTarget = $(e.currentTarget);
      this._vote(true, $currentTarget);
    },

    onVoteDown: function(e) {
      var $currentTarget = $(e.currentTarget);
      this._vote(false, $currentTarget);
    },

    _vote: function(up, icon) {
      var voted = icon.hasClass('voted');
      this.$('.voted').removeClass('voted');
      if (voted) {
        this.model.unvote().success(function(){

        });
      } else {
        
        this.model.vote(up).success(function(){
          icon.addClass('voted');
        });
      }

    },

    onClickShowCommentForm: function(e) {
      $(e.currentTarget).remove();

      this.ui.sendComment.removeClass('hide');
      this.commentForm.buildControl('content', this.ui.commentForm, {
        height: 100
      });
    },

    onSend: function(e) {
      var self = this;

      var $currentTarget = $(e.currentTarget);
      $currentTarget.bsbutton('loading');

      this.comment.save().complete(function(){
        $currentTarget.bsbutton('reset');
      }).success(function(){
        self.commentForm.getControl('content').markdownEditor.setValue('');
        self.comment.id = void 0;
      });
    }
  });

  return ItemView;
});