define([
  'underscore.custom'
  , 'marionette.custom'
  , 'views/mixins/model_binding'
], function(_, Marionette, modelBinding){
  var View = Marionette.View.extend({
    template: '<input class="form-control"/>',
    delay: 300,

    events: {
      'keyup': 'onKeyup',
      'keyup input': 'onKeyup'
    },

    initialize: function() {
      this._changing = false;
      var attribute = this.getOption('attribute');
      this.listenTo(this.model, 'change:'+attribute, this.onChangeModelValue);
    },

    render: function() {
      var template = _.result(this, 'template');
      
      this.$el.html(template);
      this.$input = this.$('input');
      this.setValue(this.getModelValue());
    },

    onKeyup: function(e) {
      var attribute = this.getOption('attribute');
      var self = this;
      this.runOnce(function(){
        var val = self.getValue();
        self._changing = true;
        self.setModelValue(val);
        self._changing = false;
      }, this.getOption('delay'));
    },

    getValue: function() {
      return this.$input.val();
    },

    setValue: function(value) {
      this.$input.val(value);
    },

    onChangeModelValue: function(model, newValue) {
      if (this._changing) {
        return;
      }
      this.setValue(newValue);
    }
  });

  _.extend(View.prototype, modelBinding);

  return View;
});