define([
  'views/common/edit_modal'
  , 'views/common/question_edit'
], function(EditModal, EditView){
  return EditModal.extend({
    template: '#question-edit-modal-template',
    editView: EditView
  });
})