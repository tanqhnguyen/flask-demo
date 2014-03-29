define([
  'marionette.custom'
  , 'views/common/article'
], function(Marionette, ArticleView){

  var CollectionView = Marionette.CollectionView.extend({
    itemView: ArticleView
  });

  return CollectionView;
});