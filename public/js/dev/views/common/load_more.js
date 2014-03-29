define([
  'underscore.custom'
  , 'marionette.custom'
  , 'views/common/empty'
], function(_, Marionette, EmptyView){

  var CollectionView = Marionette.CollectionView.extend({
    events: {
      'click .js-load-more': 'onClickLoadMore'
    },

    emptyView: EmptyView,

    /*
      {'article_id': 'id'}
    */
    modelData: {},

    data: {},

    fetchMethod: 'fetch',

    template: function() {
      return _.template('<div class="js-entries"></div><div><button autocomplete="off" class="btn btn-primary btn-sm js-load-more form-control"><%= _.t("Load More") %></button></div>');
    },

    onBeforeRender: function() {
      this.$el.html(this.template());

      var size = this.collection.size();
      var limit = this.collection.getLimit();

      if (size < limit) {
        this.$('.js-load-more').hide();
      }
    },

    appendHtml: function(collectionView, itemView, index){
      if (collectionView.isBuffering) {
        // buffering happens on reset events and initial renders
        // in order to reduce the number of inserts into the
        // document, which are expensive.
        collectionView.elBuffer.appendChild(itemView.el);
      }
      else {
        // If we've already rendered the main collection, just
        // append the new items directly into the element.
        collectionView.$('.js-entries').append(itemView.el);
      }
    },

    appendBuffer: function(collectionView, buffer) {
      collectionView.$('.js-entries').append(buffer);
    },

    _constructRequestData: function(data) {
      var modelData = Marionette.getOption(this, 'modelData');

      _.each(modelData, function(v, k){
        data[k] = this.model.get(v);
      }, this);

      var d = Marionette.getOption(this, 'data');

      _.each(d, function(v, k){
        data[k] = v;
      });

      return data;
    },

    fetchCollection: function(options) {
      var self = this;

      options = options || {};

      options.data = options.data || {};
      this._constructRequestData(options.data);

      var fetchMethod = Marionette.getOption(this, 'fetchMethod');

      return this.collection[fetchMethod](options).success(function(response){
        self.triggerMethod('fetch', response);
      });
    },

    onClickLoadMore: function(e) {
      var self = this;

      var $currentTarget = $(e.currentTarget);
      $currentTarget.bsbutton('loading');

      var collection = this.collection;
      var currentOffset = collection.getOffset();
      var limit = collection.getLimit();
      var offset = currentOffset + limit;



      this.fetchCollection({
        add: true,
        remove: false,
        data: {
          offset: offset,
          limit: limit
        }
      }).complete(function(){
        var disabled = self.collection.pagination.offset - self.collection.pagination.total >= 0
        var nextOffset = self.collection.getOffset() + self.collection.getLimit();
        disabled = disabled || nextOffset > self.collection.pagination.total;
        $currentTarget.bsbutton('reset');  
        if (disabled) {
          $currentTarget.hide();
        }
      }).error(function(){
        
      });
    },

    onRefresh: function() {
      this.$('.js-load-more').show();
      this.fetchCollection({
        reset: true
      });
    }
  });

  return CollectionView;
});