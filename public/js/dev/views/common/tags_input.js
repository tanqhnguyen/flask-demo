define([
  'underscore.custom'
  , 'marionette.custom'
  , 'views/mixins/model_binding'
  , 'vendors/select2'
], function(_, Marionette, modelBinding){
  var View = Marionette.ItemView.extend({
    template: function() {

    },

    maximumSelectionSize: 5,
    placeholder: _.t('at least 1 tag, maxium 5 tags'),
    tokenSeparators: [",", " "],

    onRender: function() {
      var self = this;

      this.$el.select2({
        tags: true,
        initSelection : function (element, callback) {
          var data = [];
          $(element.val().split(",")).each(function () {
              data.push({id: this, text: this});
          });
          callback(data);
        },
        tokenSeparators: Marionette.getOption(this, 'tokenSeparators'),
        maximumSelectionSize: Marionette.getOption(this, 'maximumSelectionSize'),
        placeholder: Marionette.getOption(this, 'placeholder'),
        createSearchChoice: function(term, data) {
          if ($(data).filter(function() { return this.text.localeCompare(term)===0; }).length===0) {
            return {id:term, text:term};
          }
        },
        ajax: {
          url: '/api/tags/autocomplete',
          dataType: "json",
          data: function(term, page) {
            return {
              query: term
            };
          },
          results: function(response, page) {
            var results = [];
            _.each(response.data, function(data){
              results.push({
                id: data.name,
                text: data.name
              });
            });
            return {
              results: results
            };
          }
        }
      });

      this.$el.on('change', function(e){
        self.setModelValue(self.getValue());
      });

      var values = this.options.values || this.getModelValue();

      if (!_.isArray(values)) {
        values = [values];
      }
      if (values.length > 0) {
        this.setValue(values);
      }
      
    },

    getValue: function() {
      return this.$el.select2('val');
    },

    setValue: function(values) {
      if (values.length == 0) {
        return this;
      }
      this.$el.select2('val', values);
      return this;
    },

    show: function() {
      this.$el.select2('container').show();
    },

    hide: function() {
      this.$el.select2('container').hide();
    }
  });

  _.extend(View.prototype, modelBinding);

  return View;
});