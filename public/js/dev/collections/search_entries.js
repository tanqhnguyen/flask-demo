define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basecollection'
], function(_, Backbone, BaseCollection){
  return BaseCollection.extend({
    search: function(options) {
      options = options || {};
      var self = this;
      var url = _.result(this, 'url');
      return Backbone.callApi('GET', [url, 'search'].join('/'), options.data).success(function(response){
        self.setPagination(response.pagination);

        if (options.reset) {
          self.reset(response.data);
        } else {
          self.push(response.data);  
        }
      });
    }
  });
});