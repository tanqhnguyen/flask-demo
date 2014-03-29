define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basemodel'
], function(_, Backbone, BaseModel){
  var Model = BaseModel.extend({
    url: 'users',

    getAvatar: function(size) {
      size = size || 100;
      return [Backbone.apiPrefix, this.url, 'avatar'].join('/') + '?id=' + this.id + '&size=' + size;
    },

    hasPermission: function(perm) {
      var permissions = this.get('permissions') || [];
      return _.indexOf(permissions, perm) != -1;
    },

    ban: function() {
      return this.callApi('post', 'ban', {
        id: this.id
      });
    }
  });

  return Model;
});