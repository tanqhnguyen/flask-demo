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
    url: 'articles',

    relations: {
      'user': User,
      'comments': Comments
    },

    name: 'article',

    generateContent: function() {
      return marked(this.get('content'), { renderer: marked.getRenderer('article') });
    },

    firstParagraph: function() {
      var content = this.get('content');
      content = content.split('\n')[0];
      return marked(content, { renderer: marked.getRenderer('article') });
    },

    approve: function() {
      return Backbone.callApi('post', this.url+'/approve', {
        id: this.id
      });
    },

    allowEdit: function() {
      return window.currentUser.hasPermission('update_article') || this.get('user_id') === currentUser.id;
    }
  });

  _.extend(Model.prototype, taggable, votable);

  return Model;
});