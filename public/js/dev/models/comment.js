define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basemodel'
  , 'models/user'
  , 'libs/marked'
], function(_, Backbone, BaseModel, User, marked){
  var Model = BaseModel.extend({
    url: function(){
      if (this.collection) {
        return this.collection.url();
      }
      
      if (this.get('article_id')) {
        return 'articles/comments';
      } else if (this.get('question_id')) {
        return 'questions/comments';
      } else if (this.get('answer_id')) {
        return 'questions/answers/comments';
      } else if (this.get('topic_id')) {
        return 'topics/comments';
      }
    },

    initialize: function() {
      
    },

    relations: {
      'user': User
    },

    generateContent: function() {
      return marked(this.get('content'), { renderer: marked.getRenderer('comment') });
    },

    allowDelete: function() {
      return _.hasPermission('delete_comment')
    }
  });

  return Model;
});