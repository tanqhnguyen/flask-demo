require([
  'views/tags/main'
  , 'collections/articles'
  , 'collections/topics'
], function(MainView, Articles, Topics){
  var view = new MainView({
    el: '#tags',
    articles: window.appData.articles,
    topics: [],
    tag: window.appData.tag
  });

  view.render();
});