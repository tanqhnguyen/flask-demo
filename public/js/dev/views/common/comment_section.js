// A common view for comments including comment form and comment list
define([
  'backbone.custom'
  , 'marionette.custom'
  , 'models/comment'
  , 'views/common/comment'
  , 'views/common/load_more'
  , 'views/common/markdown_editor'
], function(Backbone, Marionette, Comment, CommentView, LoadMoreView, MarkdownEditorView){
  var View = Marionette.ItemView.extend({
    template: '#comment-section-template',

    refKey: null,

    events: {
      'click .js-send': 'onSend',
      'click .js-refresh': 'onClickRefresh'
    },

    ui: {
      commentForm: '.js-comment-form',
      commentList: '.js-comment-list',
      commentCount: '.js-comment-count'
    },

    initialize: function() {

    },

    onRender: function() {
      var self = this;
      refKey = Marionette.getOption(this, 'refKey');
      this.comment = new Comment();
      this.comment.set(refKey, this.model.id);

      var modelData = {};
      modelData[refKey] = 'id';

      this.commentsView = new LoadMoreView({
        model: this.model,
        collection: this.model.get('comments'),
        el: this.ui.commentList,
        itemView: CommentView,
        modelData: modelData
      });

      this.listenTo(this.commentsView, 'fetch', function(response){
        self.model.set('comment_count', response.pagination.total);
      });

      this.markdownEditor = new MarkdownEditorView({
        el: this.ui.commentForm,
        model: this.comment,
        attribute: 'content',
        showToolbar: false,
        lineNumbers: false,
        height: '200px'
      });

      this.markdownEditor.render();

      this.commentsView.render();
    },

    onSend: function(e) {
      var self = this;

      var $currentTarget = $(e.currentTarget);
      $currentTarget.bsbutton('loading');

      this.comment.save().complete(function(){
        $currentTarget.bsbutton('reset');
      }).success(function(){
        self.markdownEditor.setValue('');
        self.comment.id = void 0;
        self.onClickRefresh();
      })
    },

    onClickRefresh: function(e) {
      this.commentsView.triggerMethod('refresh');
    }
  });

  return View;
})