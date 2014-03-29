require([
  'views/home/main'
  , 'collections/articles'
], function(MainView, Articles){
  var view = new MainView({
    el: '#home',
    collection: new Articles(window.appData.articles)
  });

  view.render();
});