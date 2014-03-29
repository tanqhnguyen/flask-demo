require([
  'views/submit_article/main'
], function(MainView){
  var view = new MainView({
    el: '#submit-article'
  });

  view.render();
});