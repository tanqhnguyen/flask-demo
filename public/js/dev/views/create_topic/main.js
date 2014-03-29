define([
  'marionette.custom'
  , 'models/topic'
  , 'views/common/topic_edit'
], function(Marionette, Topic, TopicEditView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {
      'click .js-submit': 'onCreateTopic'
    },

    initialize: function(options) {
      this.model = new Topic({
        tags: []
      });
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    ui: {
      topic: '.js-topic'
    },

    onRender: function(){
      this.editView = new TopicEditView({
        model: this.model,
        el: this.ui.topic
      });
      this.editView.render();
    },

    onCreateTopic: function(e) {
      var $target = $(e.currentTarget);
      $target.bsbutton('loading');

      this.model.save().success(function(){

      }).error(function(){
        $target.bsbutton('reset');
      });

    }
  });

  return View;
});