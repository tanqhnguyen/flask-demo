define([
  'views/common/edit_modal'
  , 'views/common/article_edit'
], function(EditModal, EditView){
  return EditModal.extend({
    template: '#article-edit-modal-template',
    editView: EditView
  });
})