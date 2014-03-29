define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basemodel'
  , 'models/user'
  , 'collections/comments'
  , 'libs/marked'
  , 'models/mixins/votable'
], function(_, Backbone, BaseModel, User, Comments, marked, votable){

  var Model = BaseModel.extend({
    url: 'questions/answers',

    relations: {
      'user': User,
      'comments': Comments
    },

    generateContent: function() {
      return marked(this.get('content'), { renderer: marked.getRenderer('comment') });
    }
  });

  _.extend(Model.prototype, votable);

  return Model;
});