require([
  'views/search/main'
], function(MainView, Articles){
  var view = new MainView({
    el: '#search',
    articles: window.appData.articles,
    topics: [],
    search: window.appData.search
  });

  view.render();
});