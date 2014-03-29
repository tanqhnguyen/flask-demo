define([
  'underscore.custom'
  , 'marionette.custom'
  , 'views/mixins/model_binding'
  , 'text!templates/common/markdown_editor.html'
  , 'vendors/codemirror'
  , 'vendors/marked'
  , 'vendors/highlight'
], function(_, Marionette, modelBinding, template, CodeMirror, marked){
  var View = Marionette.ItemView.extend({
    template: function(data) {
      return _.template(template, data);
    },

    theme: 'blackboard',
    height: '450px',
    width: '100%',
    showToolbar: true,
    lineNumbers: true,

    events: {
      'click .js-editor-control button': 'onChangeMode',
      'click .js-change-theme': 'onChangeTheme'
    },

    ui: {
      editor: '.js-editor',
      control: '.js-editor-control',
      preview: '.js-editor-preview'
    },

    initialize: function() {
      this._changing = false;
      var attribute = Marionette.getOption(this, 'attribute');
      this.listenTo(this.model, 'change:'+attribute, this.onChangeModelValue);
    },

    onRender: function() {
      var attribute = Marionette.getOption(this, 'attribute');
      var self = this;
      this.$el.css('min-height', Marionette.getOption(this, 'height'));
      this.$el.width(Marionette.getOption(this, 'width'));

      var codemirror = CodeMirror(this.ui.editor[0], {
        indentUnit: 2,
        indentWithTabs: false,
        mode:  "markdown",
        lineNumbers: Marionette.getOption(this, 'lineNumbers')
      });
      codemirror.setOption('theme', Marionette.getOption(this, 'theme'));

      codemirror.on('change', function(instance, changeObj){
        self.runOnce(function(){
          // prevent circular events with onChangeModelValue
          self._changing = true;
          self.setModelValue(self.getValue());
          self._changing = false;
        }, 1000);
      });

      this.codemirror = codemirror;

      var showToolbar = Marionette.getOption(this, 'showToolbar');
      if (!showToolbar) {
        this.ui.control.remove();
      }

      this.adjustSize();
      this.setValue(this.getModelValue());

      $(window).resize(function(){
        clearTimeout($(this).data(self.cid));
        $(this).data(self.cid, setTimeout(function(){
          self.adjustSize();
        }, 300));
      });
    },

    onChangeTheme: function(e) {
      var $target = $(e.currentTarget);
      var theme = $target.data('theme');

      this.codemirror.setOption('theme', theme);

      e.preventDefault();
    },

    onChangeMode: function(e) {
      var $target = $(e.currentTarget);

      var mode = $target.data('mode');

      if (mode) {
        this.ui.control.find('.active').removeClass('active');
        $target.addClass('active');
      }

      switch(mode) {
        case 'markdown':
          this.ui.preview.hide();
          this.ui.editor.show();
          break;
        case 'preview':
          this.ui.editor.hide();
          this.triggerMethod('preview');
          break;
        default:
          break;
      }
    },

    onChangeModelValue: function(model, newValue) {
      if (this._changing) {
        return;
      }
      this.setValue(newValue);
    },

    onPreview: function() {
      var value = this.codemirror.getValue();

      var html = marked(value, { renderer: marked.getRenderer('article') });

      this.ui.preview.html(html);
      this.ui.preview.show();
    },

    getValue: function() {
      return this.codemirror.getValue();
    },

    setValue: function(content) {
      if (!_.isUndefined(content)) {
        this.codemirror.setValue(content);  
      }
      return this;
    },

    show: function() {
      this.$el.show();
    },

    hide: function() {
      this.$el.hide();
    },

    adjustSize: function() {
      this.codemirror.setSize(this.ui.editor.width(), this.$el.height() - this.ui.control.height());
    }
  });

  _.extend(View.prototype, modelBinding);

  return View;
});