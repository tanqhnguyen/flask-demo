define([
  'vendors/marked'
  , 'vendors/highlight'
], function(marked){
  /* Renderer for parsing comments */
  var commentRenderer = new marked.Renderer();

  commentRenderer.heading = function (text, level) {
    return text;
  };

  /* Article renderer */
  var articleRenderer = new marked.Renderer();

  articleRenderer.heading = function (text, level) {
    if (level < 3) {
      level = 3;
    }

    return '<h' + level + '>' + text + '</h' + level + '>';
  };

  var renderers = {
    comment: commentRenderer,
    article: articleRenderer
  }

  marked.setOptions({
    sanitize: true,
    highlight: function (code) {
      return hljs.highlightAuto(code).value;
    }
  });

  marked.getRenderer = function(name) {
    return renderers[name];
  }

  return marked;
})