define([
  'basecollection'
  , 'models/question'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    model: Model
  });
});