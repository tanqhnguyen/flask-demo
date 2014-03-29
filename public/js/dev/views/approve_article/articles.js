define([
  'marionette.custom'
  , 'views/approve_article/article'
], function(Marionette, ArticleView){

  var CollectionView = Marionette.CollectionView.extend({
    itemView: ArticleView
  });

  return CollectionView;
});