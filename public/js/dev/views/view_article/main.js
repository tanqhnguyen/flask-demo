define([
  'backbone.custom'
  , 'marionette.custom'
  , 'views/view_article/article'
  , 'views/common/comment_section'
], function(Backbone, Marionette, ArticleView, CommentSectionView) {
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      'click .js-edit': 'onClickEdit'
    },

    ui: {
      article: '.js-article',
      commentSection: '.js-comment-section'
    },

    initialize: function() {
      var self = this;
      this.commentSection = new CommentSectionView({
        el: this.ui.commentSection,
        model: this.model,
        refKey: 'article_id'
      });

      this.articleView = new ArticleView({
        model: this.model,
        el: this.ui.article
      });
    },

    onRender: function(){
      this.articleView.render();
      this.commentSection.render();
    },

    onClickEdit: function() {
      var self = this;
      require([
        'views/common/article_edit_modal'
      ], function(ArticleEditModalView){
        var view = new ArticleEditModalView({
          model: self.model
        });

        view.render();
      });
    }
  });

  return View;
});