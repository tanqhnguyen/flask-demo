require([
  'views/create_topic/main'
], function(MainView){
  var view = new MainView({
    el: '#create-topic'
  });

  view.render();
});