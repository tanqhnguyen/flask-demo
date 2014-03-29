define([
  'underscore.custom'
  , 'backbone.custom'
  , 'basemodel'
  , 'models/user'
  , 'collections/comments'
  , 'libs/marked'
  , 'models/mixins/taggable'
  , 'models/mixins/votable'
], function(_, Backbone, BaseModel, User, Comments, marked, taggable, votable){

  var Model = BaseModel.extend({
    url: 'topics',

    relations: {
      'user': User,
      'comments': Comments
    },

    name: 'topic',

    generateContent: function() {
      return marked(this.get('content'), { renderer: marked.getRenderer('article') });
    }
  });

  _.extend(Model.prototype, taggable, votable);

  return Model;
});