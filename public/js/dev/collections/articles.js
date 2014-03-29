define([
  'basecollection'
  , 'models/article'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    model: Model
  });
});