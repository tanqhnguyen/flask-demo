define([
  'marionette.custom'
  , 'models/article'
  , 'views/common/article_edit'
], function(Marionette, Article, ArticleEditView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      'click .js-submit': 'onSubmitArticle'
    },

    initialize: function(options) {
      this.model = new Article({
        tags: []
      });
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    ui: {
      article: '.js-article'
    },

    onRender: function(){
      this.editView = new ArticleEditView({
        model: this.model,
        el: this.ui.article
      });
      this.editView.render();
    },

    onSubmitArticle: function(e) {
      var $target = $(e.currentTarget);
      $target.bsbutton('loading');

      this.model.save().success(function(){

      }).error(function(){
        $target.bsbutton('reset');
      });

    }
  });

  return View;
});