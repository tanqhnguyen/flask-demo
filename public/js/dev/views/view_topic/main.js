define([
  'backbone.custom'
  , 'marionette.custom'
  , 'views/view_topic/topic'
  , 'views/common/comment_section'
], function(Backbone, Marionette, TopicView, CommentSectionView){
  var View = Marionette.Layout.extend({
    template: function() {

    },

    events: {

    },

    ui: {
      topic: '.js-topic',
      commentSection: '.js-comment-section'
    },

    initialize: function() {
      var self = this;
      this.commentSection = new CommentSectionView({
        el: this.ui.commentSection,
        model: this.model,
        refKey: 'topic_id'
      });

      this.topicView = new TopicView({
        model: this.model,
        el: this.ui.topic
      });
    },

    onRender: function(){
      this.topicView.render();

      this.commentSection.render();
    }
  });

  return View;
});