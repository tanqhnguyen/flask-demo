define([
  'underscore.custom'
  , 'backbone.custom'
  , 'models/mixins/moment'
], function(_, Backbone, moment){
  var Model = Backbone.SuperModel.extend({
    parse: function(response) {
      if (response.data) {
        return response.data;
      }
      return response;
    },

    callApi: function(type, url, data) {
      data = data || {};
      url = [_.result(this, 'url'), url].join('/');
      return Backbone.callApi(type, url, data);
    }
  });

  Model.prototype = _.extend(Model.prototype, moment);

  return Model;
});