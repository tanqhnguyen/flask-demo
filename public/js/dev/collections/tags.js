define([
  'basecollection'
  , 'models/question'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    url: 'tags',
    
    model: Model
  });
});