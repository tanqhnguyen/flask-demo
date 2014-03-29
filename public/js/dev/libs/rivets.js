define([
  'underscore.custom'
  , 'vendors/rivets'
  , 'libs/marked'
], function(_, rivets, marked){
  rivets.adapters[':'] = {
    subscribe: function(obj, keypath, callback) {
      obj.on('change:' + keypath, callback)
    },
    unsubscribe: function(obj, keypath, callback) {
      obj.off('change:' + keypath, callback)
    },
    read: function(obj, keypath) {
      return obj.get(keypath)
    },
    publish: function(obj, keypath, value) {
      obj.set(keypath, value)
    }
  };

  rivets.formatters.tags = function(value){
    var template = '<span class="label label-success"><a href="/tags/<%= tag %>.html" style="color: rgb(255, 255, 255);"><%= tag %></a></span>';
    var tags = value.map(function(tag){
      return _.template(template, {tag: tag.get('name')});
    });

    return tags.join(" ");
  };

  rivets.formatters.markdown = function(value, renderer) {
    renderer = renderer || 'article';
    return marked(value, { renderer: marked.getRenderer(renderer) });
  }

  return rivets;
});