require([
  'views/approve_article/main'
], function(MainView){
  var view = new MainView({
    el: '#approve-article'
  });

  view.render();
});