define([
  'marionette.custom'
  , 'collections/search_entries'
  , 'models/article'
  , 'models/topic'
  , 'views/home/article'
  , 'views/topics/topic'
  , 'views/common/load_more'
], function(Marionette, SearchEntries, Article, Topic, ArticleView, TopicView, LoadMoreView){

  var ArticleSearchEntries = SearchEntries.extend({
    model: Article,
    url: 'articles'
  });

  var TopicSearchEntries = SearchEntries.extend({
    model: Topic,
    url: 'topics'
  });

  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      
    },

    ui: {
      articles: '#articles',
      topics: '#topics'
    },

    initialize: function() {
      this.views = {};

      this.articles = new ArticleSearchEntries(this.options.articles);
      this.topics = new TopicSearchEntries(this.options.topics);
    },

    onRender: function(){
      var self = this;

      this.views.articles = new LoadMoreView({
        collection: this.articles,
        el: this.ui.articles,
        itemView: ArticleView,
        data: {
          query: this.options.search
        },
        fetchMethod: 'search'
      });
      this.views.articles.render();

      this.views.topics = new LoadMoreView({
        collection: this.topics,
        el: this.ui.topics,
        itemView: TopicView,
        data: {
          query: this.options.search
        },
        fetchMethod: 'search'
      });
      this.views.topics.render();

      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var type = $(e.target).data('type');

        var collection = self[type];

        collection.search({
          reset: true,
          data: {
            query: self.options.search
          }
        });
      })
    }
  });

  return View;
});