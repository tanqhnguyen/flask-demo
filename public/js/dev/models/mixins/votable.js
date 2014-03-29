define([
  'underscore.custom'
  , 'backbone.custom'
], function(_, Backbone){
  return {
    vote: function(up) {
      var self = this;
      if (up === void 0) {
        up = true
      }

      url = _.result(this, 'url');

      var xhr = Backbone.callApi('post', url+'/vote', {
        id: this.id,
        up: up
      });

      xhr.success(function(response){
        self.set('points', response.data.points);
      });

      return xhr;
    },

    unvote: function() {
      var self = this;

      url = _.result(this, 'url');

      var xhr = Backbone.callApi('post', url+'/unvote', {
        id: this.id
      });

      xhr.success(function(response){
        self.set('points', response.data.points);
      });

      return xhr;
    },

    hasVoted: function() {
      return this.get('user_vote') !== null;
    }
  }
})