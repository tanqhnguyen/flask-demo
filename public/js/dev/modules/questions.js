require([
  'views/questions/main'
  , 'collections/questions'
], function(MainView, Questions){
  var view = new MainView({
    el: '#questions',
    collection: new Questions(window.appData.questions)
  });

  view.render();
});