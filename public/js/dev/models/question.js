define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basemodel'
  , 'models/user'
  , 'collections/comments'
  , 'collections/answers'
  , 'libs/marked'
  , 'models/mixins/taggable'
  , 'models/mixins/votable'
], function(_, Backbone, BaseModel, User, Comments, Answers, marked, taggable, votable){

  var Model = BaseModel.extend({
    url: 'questions',

    relations: {
      'user': User,
      'comments': Comments,
      'answers': Answers
    },

    generateContent: function() {
      return marked(this.get('content'), { renderer: marked.getRenderer('article') });
    }
  });

  _.extend(Model.prototype, taggable, votable);

  return Model;

});