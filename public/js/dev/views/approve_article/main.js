define([
  'marionette.custom'
  , 'collections/articles'
  , 'views/approve_article/articles'
  , 'views/common/article_edit_modal'
], function(Marionette, Articles, ArticlesView, ArticleEditModal){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      
    },

    ui: {
      articles: '.js-articles'
    },

    initialize: function() {
      this.articles = new Articles();
    },

    onRender: function(){
      var self = this;
      this.articlesView = new ArticlesView({
        collection: this.articles,
        el: this.ui.articles
      });

      this.articlesView.render();
      
      this.articles.fetch({
        data: {
          is_active: 0
        }
      }).success(function(){

      });
    }
  });

  return View;
});