require([
  'models/topic'
  , 'views/view_topic/main'
], function(Topic, MainView){
  var view = new MainView({
    el: '#view-topic',
    model: new Topic(window.appData.topic)
  });

  view.render();
});