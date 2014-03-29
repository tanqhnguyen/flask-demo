define([
  'underscore.custom'
  , 'marionette.custom'
], function(_, Marionette){
  return Marionette.View.extend({
    render: function() {
      var self = this;
      var template = $(this.template).html();
      template = $(_.template(template, this.serializeData()));

      $('body').append(template);

      this.setElement(template);

      this.$el.modal();

      var bsEvents = [
        'shown', 'show', 'hidden', 'hide', 'loaded'
      ];

      _.each(bsEvents, function(e){
        this.$el.on(e+'.bs.modal', function(){
          self.triggerMethod(e);
        });
      }, this);
      
      this.$el.on('hidden.bs.modal', function(){
        self.$el.remove();
      });

      this.triggerMethod('render');
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    hide: function() {
      this.$el.modal('hide');
    },

    show: function() {
      this.$el.modal('show');
    }
  });
})