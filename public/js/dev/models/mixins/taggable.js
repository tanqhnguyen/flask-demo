define([
  'underscore.custom'
], function(_){
  return {
    generateTagArray: function() {
      var tags = this.get('tags');
      if (_.isArray(tags)) {
        return tags;
      }
      return tags.map(function(tag){
        return tag.get('name')
      });
    },

    // set new tags and remove old tags
    setTags: function(attribute, tags) {
      if (!_.isArray(tags)) {
        tags = [tags];
      }

      tags = _.map(tags, function(tag){
        return {
          name: tag
        }
      });

      this.get('tags').reset(tags);
    }
  }
})