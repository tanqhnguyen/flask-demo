define([
  'marionette.custom'
  , 'views/common/edit'
  , 'forms/question_edit'
], function(Marionette, EditView, Form){

  var ItemView = EditView.extend({
    template: '#question-edit-template',
    formClass: Form
  });

  return ItemView;
});