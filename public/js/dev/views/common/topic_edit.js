define([
  'marionette.custom'
  , 'views/common/markdown_editor'
  , 'views/common/text_input'
  , 'views/common/tags_input'
], function(Marionette, MarkdownEditorView, TextInputView, TagsInputView){

  var ItemView = Marionette.ItemView.extend({
    template: '#topic-edit-template',

    events: {

    },

    initialize: function() {

    },

    ui: {
      tags: '.js-tags',
      title: '.js-title',
      content: '.js-content'
    },

    serializeData: function() {
      return {
        model: this.model
      };
    },

    onRender: function() {
      var self = this;

      this.markdownEditor = new MarkdownEditorView({
        el: this.ui.content,
        model: this.model,
        attribute: 'content'
      });
      this.markdownEditor.render();

      this.textInput = new TextInputView({
        el: this.ui.title,
        model: this.model,
        attribute: 'title'
      });
      this.textInput.render();

      this.tagsInput = new TagsInputView({
        el: this.ui.tags,
        model: this.model,
        attribute: 'tags',
        set: 'setTags',
        get: 'generateTagArray'
      });

      this.tagsInput.render();
    }
  });

  return ItemView;
});