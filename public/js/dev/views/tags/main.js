define([
  'marionette.custom'
  , 'collections/tags'
  , 'models/article'
  , 'models/topic'
  , 'views/articles/article'
  , 'views/topics/topic'
  , 'views/common/load_more'
], function(Marionette, Tags, Article, Topic, ArticleView, TopicView, LoadMoreView){

  var TagArticles = Tags.extend({
    model: Article
  });

  var TagTopics = Tags.extend({
    model: Topic
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

      this.articles = new TagArticles(this.options.articles);
      this.topics = new TagTopics(this.options.topics);
    },

    onRender: function(){
      var self = this;

      this.views.articles = new LoadMoreView({
        collection: this.articles,
        el: this.ui.articles,
        itemView: ArticleView,
        data: {
          name: this.options.tag,
          type: 'articles'
        }
      });
      this.views.articles.render();

      this.views.topics = new LoadMoreView({
        collection: this.topics,
        el: this.ui.topics,
        itemView: TopicView,
        data: {
          name: this.options.tag,
          type: 'topics'
        }
      });
      this.views.topics.render();

      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var type = $(e.target).data('type');

        Backbone.callApi('GET', 'tags/list', {
          name: self.options.tag,
          type: type          
        }).success(function(response){
          var collection = self[type];
          collection.setPagination(response.pagination);
          collection.reset(response.data);
        });
      })
    }
  });

  return View;
});