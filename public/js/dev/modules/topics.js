require([
  'views/topics/main'
  , 'collections/topics'
], function(MainView, Topics){
  var view = new MainView({
    el: '#topics',
    collection: new Topics(window.appData.topics)
  });

  view.render();
});