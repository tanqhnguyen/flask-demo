define([
  'moment'
], function(moment){
  return {
    moment: function(attr) {
      return moment(this.get(attr));
    },

    relativeTime: function(attr) {
      return moment(this.get(attr)).fromNow();
    }
  }
});  