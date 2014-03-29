define([
  'marionette.custom'
  , 'views/topics/topic'
  , 'views/common/load_more'
], function(Marionette, TopicView, LoadMoreView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      
    },

    ui: {
      topics: '.js-topics'
    },

    initialize: function() {
      
    },

    onRender: function(){
      var self = this;
      
      this.topicsView = new LoadMoreView({
        collection: this.collection,
        el: this.ui.topics,
        itemView: TopicView
      });
      this.topicsView.render();

      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var order = $(e.target).data('order');
        self.collection.fetch({
          reset: true,
          data: {
            order: order
          }
        });
      })
    }
  });

  return View;
});