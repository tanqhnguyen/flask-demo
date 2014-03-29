define([
  'basecollection'
  , 'models/topic'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    model: Model
  });
});