define([
  'marionette.custom'
  , 'libs/rivets'
], function(Marionette, rivets){

  var ItemView = Marionette.ItemView.extend({
    template: '#article-template',

    className: 'article preview',

    events: {
      'click .js-vote-up': 'onVoteUp',
      'click .js-vote-down': 'onVoteDown'
    },

    initialize: function() {

    },

    ui: {
      tags: '.js-tags',
      content: '.js-content',
      author: '.js-author',
      sidebar: '.js-sidebar',
      votePoints: '.js-vote-points',
      voteUp: '.js-vote-up',
      voteDown: '.js-vote-down',
      commentCount: '.js-comment-count',
      viewCount: '.js-view-count'
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    onRender: function() {
      var self = this;

      rivets.bind(this.$el, {
        model: this.model
      });
    },

    onVoteUp: function(e) {
      var $currentTarget = $(e.currentTarget);
      this._vote(true, $currentTarget);
    },

    onVoteDown: function(e) {
      var $currentTarget = $(e.currentTarget);
      this._vote(false, $currentTarget);
    },

    _vote: function(up, icon) {
      var voted = icon.hasClass('voted');
      this.$('.voted').removeClass('voted');
      if (voted) {
        this.model.unvote().success(function(){

        });
      } else {
        
        this.model.vote(up).success(function(){
          icon.addClass('voted');
        });
      }

    }
  });

  return ItemView;
});