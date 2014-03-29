// any view that needs to interact with model must use this mixin
define([

], function(){
  return {
    get: 'get',
    set: 'set',

    getModelValue: function() {
      var attribute = this.getOption('attribute');
      var get = this.getOption('get');
      return this.model[get](attribute);
    },

    setModelValue: function(value) {
      this.triggerMethod('change', value);
      var attribute = this.getOption('attribute');
      var set = this.getOption('set');
      return this.model[set](attribute, value);
    }
  }
});