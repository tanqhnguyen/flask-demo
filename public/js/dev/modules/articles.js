require([
  'views/articles/main'
  , 'collections/articles'
], function(MainView, Articles){
  var view = new MainView({
    el: '#articles',
    collection: new Articles(window.appData.articles)
  });

  view.render();
});