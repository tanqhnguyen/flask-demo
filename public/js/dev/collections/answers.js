define([
  'basecollection'
  , 'models/answer'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    model: Model
  });
});