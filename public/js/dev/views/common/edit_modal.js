// General class for editable content in bootstrap modal

define([
  'marionette.custom'
  , 'views/common/modal'
], function(Marionette, Modal){
  return Modal.extend({
    editView: null,

    events: {
      'click .js-save': 'onClickSave'
    },

    onRender: function() {
      var self = this;

      this.$('.modal-dialog').css({
        width: '100%'
      });

      var editView = Marionette.getOption(this, 'editView');

      this.editView = new editView({
        model: this.model,
        el: this.$('.modal-body')
      });
    },

    onShown: function() {
      this.editView.render();
    },

    onClickSave: function(e) {
      var self = this;
      var $currentTarget = $(e.currentTarget);

      $currentTarget.bsbutton('loading');

      this.model.save().complete(function(){
        $currentTarget.bsbutton('reset');
      }).success(function(){
        self.hide();
      });
    }
  });
})