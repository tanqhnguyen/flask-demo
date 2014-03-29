define([
  'marionette.custom'
  , 'views/home/article'
  , 'views/common/load_more'
], function(Marionette, ArticleView, LoadMoreView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      
    },

    ui: {
      articles: '.js-articles'
    },

    initialize: function() {
      
    },

    onRender: function(){
      var self = this;

      this.articlesView = new LoadMoreView({
        collection: this.collection,
        el: this.ui.articles,
        itemView: ArticleView
      });
      this.articlesView.render();

      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var order = $(e.target).data('order');
        self.collection.fetch({
          reset: true,
          data: {
            order: order
          }
        });
      })
    }
  });

  return View;
});