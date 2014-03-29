define([
  'underscore'
  , 'backbone'
  , 'vendors/backbone.supermodel'
  , 'vendors/arrg'
  , 'vendors/jquery.noty'
  , 'vendors/jquery.noty.top'
  , 'vendors/jquery.noty.bootstrap'
], function(_, Backbone, SuperModel, arrg, noty){
  Backbone.SuperModel = SuperModel;

  Backbone.arrg = arrg;

  Backbone.showAlert = function(type, messages) {
    // wtf is this mess?
    if (_.isArray(messages)) {
      var _messages = [];
      _.each(messages, function(message){
        if (_.isString(message)) {
          _messages.push(message)
        } else {
          message = _.values(message);
          message = _.flatten(message);
          _messages = _.union(_messages, message);
        }
      });
      messages = _messages.join("<br/>");
    } else if (_.isObject(messages)) {
      var values = _.values(messages);
      values = _.flatten(values);
      messages = values.join("<br/>");
    }

    var options = {
      text: messages,
      type: type,
      timeout: 2000,
      layout: 'top'
    };

    noty(options);
  }

  Backbone.Dispatch = _.extend({}, Backbone.Events);

  Backbone.Dispatch.on('error', function(messages){
    Backbone.showAlert('error', messages);
  });

  Backbone.Dispatch.on('success', function(messages){
    Backbone.showAlert('success', messages);
  });

  Backbone.Dispatch.on('unauthorizeAccess', function(messages){
    $('#login-dialog').modal({
      backdrop: 'static'
    });
  });

  var methodMap = {
    'create': 'POST',
    'update': 'POST',
    'delete': 'POST',
    'read':   'GET',
    'list': 'GET'
  };

  var apiPrefix = '/api';

  Backbone.apiPrefix = apiPrefix;

  Backbone.wrapError = function(model, options) {
    var error = options.error;
    options.error = function(resp) {
      if (error) error(model, resp, options);
      model.trigger('error', model, resp, options);
    };
  }

  Backbone.sync = function(method, model, options) {
    var type = methodMap[method];

    // Default options, unless specified.
    _.defaults(options || (options = {}), {
      emulateHTTP: Backbone.emulateHTTP,
      emulateJSON: Backbone.emulateJSON
    });

    // Default JSON-request options.
    var params = {type: type, dataType: 'json'};

    // Ensure that we have a URL.
    if (!options.url) {
      params.url = _.result(model, 'url');
    }

    if (!params.url) {
      throw "URL is not defined";
    }

    params.url = '/' + params.url + '/' + method;

    // Ensure that we have the appropriate request data.
    if (options.data == null && model && (method === 'create' || method === 'update' || method === 'patch' || method === 'delete')) {
      params.contentType = 'application/json';
      params.data = options.attrs || model.toJSON(options);
    } else {
      params.data = options.data;
    }

    // Don't process data on a non-GET request.
    if (params.type !== 'GET' && !options.emulateJSON) {
      params.processData = false;
    }

    // Make the request, allowing the user to override any Ajax options.
    //var xhr = options.xhr = Backbone.ajax(_.extend(params, options));
    var xhr = options.xhr = Backbone.callApi(params.type, params.url, params.data, options);
    model.trigger('request', model, xhr, options);
    return xhr;
  };

  Backbone.parseApiError = function(xhr) {
    try {
      var error = JSON.parse(xhr.responseText).error;
      return error;
    } catch (e) {
      return {
        type: "NETWORK_ERROR",
        messages: _.t("Network Error")
      };
    }
  }

  Backbone.callApi = function(type, uri, data, options) {
    type = type.toLowerCase();
    data = data || {};
    options = options || {};

    if (uri.charAt(0) != '/') {
      uri = '/' + uri;
    }

    uri = apiPrefix + uri;

    var params = _.extend({
      type: type,
      url: uri,
      dataType: 'json'
    }, options);

    if (type == 'post') {
      params['contentType'] = 'application/json';
      params['data'] = JSON.stringify(data);
    } else {
      params['data'] = data;
    }

    var xhr = $.ajax(params);

    if (!options.customError) {
      xhr.error(function(xhr){
        var error = Backbone.parseApiError(xhr);
        if (error.type == 'UNAUTHORIZED_ACCESS') {
          Backbone.Dispatch.trigger('unauthorizeAccess');
        }
        Backbone.Dispatch.trigger('error', error.messages);
      });      
    }

    xhr.success(function(response){
      if (response.alert) {
        Backbone.Dispatch.trigger(response.alert.type, response.alert.messages);
      }

      if (response.redirect) {
        setTimeout(function(){
          window.location.href = response.redirect;
        }, 2000);
      }
    });


    return xhr;
  }

  return Backbone;
});