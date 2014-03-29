define([
  'basecollection'
  , 'models/comment'
], function(BaseCollection, Model){
  return BaseCollection.extend({
    model: Model,

    url: function() {
      if (this.article) {
        return 'articles/comments';
      } else if (this.question) {
        return 'questions/comments';
      } else if (this.answer) {
        return 'questions/answers/comments';
      } else if (this.topic) {
        return 'topics/comments';
      }
    },

    comparator: function(model) {
      return -model.get('date_created');
    }
  });
});