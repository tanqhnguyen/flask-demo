define([
  'underscore.custom'
  , 'backbone.custom'
], function(_, Backbone){
  return Backbone.Collection.extend({
    model: Backbone.SuperModel,
    pagination: {},
    defaultLimit: 10,

    url: function() {
      var url = this.model.prototype.url;
      if (_.isFunction(url)) {
        return url();
      }
      return url;
    },

    fetch: function(options) {
      options = options ? _.clone(options) : {};
      if (options.parse === void 0) options.parse = true;
      var success = options.success;
      var collection = this;
      options.success = function(resp) {
        var method = options.reset ? 'reset' : 'set';
        collection[method](resp, options);
        if (success) success(collection, resp, options);
        collection.trigger('sync', collection, resp, options);
      };
      Backbone.wrapError(this, options);
      return this.sync('list', this, options);
    },

    getOffset: function() {
      var offset = this.pagination.offset;
      return offset === void 0 ? 0 : offset;
    },

    setOffset: function(offset) {
      this.pagination.offset = offset;
    },

    getLimit: function() {
      var limit = this.pagination.limit;
      return limit === void 0 ? this.defaultLimit : limit;
    },

    setLimit: function(limit) {
      this.pagination.limit = limit;
    },

    setPagination: function(pagination) {
      this.pagination = pagination;
    },

    parse: function(response, options) {
      this.setPagination(response.pagination);
      return response.data;
    }
  });
});