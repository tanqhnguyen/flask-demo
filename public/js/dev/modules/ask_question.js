require([
  'views/ask_question/main'
], function(MainView){
  var view = new MainView({
    el: '#ask-question'
  });

  view.render();
});