require([
  'models/question'
  , 'views/view_question/main'
], function(Question, MainView){
  var view = new MainView({
    el: '#view-question',
    model: new Question(window.appData.question)
  });

  view.render();
});