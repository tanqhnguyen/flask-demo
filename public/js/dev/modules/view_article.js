require([
  'models/article'
  , 'views/view_article/main'
], function(Article, MainView){
  var view = new MainView({
    el: '#view-article',
    model: new Article(window.appData.article)
  });

  view.render();
});