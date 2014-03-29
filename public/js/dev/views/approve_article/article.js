define([
  'views/view_article/article'
  , 'views/common/article_edit_modal'
], function(ArticleView, ArticleEditModalView){
  var View = ArticleView.extend({
    className: 'article pending',

    events: _.extend(ArticleView.prototype.events, {
      'click .js-edit': 'onClickEdit',
      'click .js-reject': 'onClickReject',
      'click .js-approve': 'onClickApprove'
    }),

    onRender: function() {
      ArticleView.prototype.onRender.apply(this, arguments);

      this.ui.sidebar.append($('#sidebar-action-template').html());
    },

    onClickEdit: function(e) {
      this.modal = new ArticleEditModalView({
        model: this.model
      });
      this.modal.render();
    },

    onClickReject: function(e) {
      var self = this;

      this.model.destroy({wait: true}).complete(function(){
        
      }).success(function(){
        
      });
    },

    onClickApprove: function(e) {
      var self = this;

      this.model.approve().complete(function(){
        
      }).success(function(){
        self.model.collection.remove(self.model);
      });
    }
  });

  return View;
});