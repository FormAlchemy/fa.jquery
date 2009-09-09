(function($) {
$.extend({fa:{}});
$.extend($.fa, {
  autocomplete: function(field, plugin, options) {
    plugin.remove();
    var data = options.data;
    delete options.data;
    field.autocomplete(data, options);
  },
  selectable: function(options) {
    var field = $(document.getElementById(options.name));
    var selectable = $(document.getElementById(options.name+'_selectable'));
    var error = $(document.getElementById(options.name+'_error'));
    var initValue = function() {
      if (!options.multiple) {
          var value = field.val();
          $('li', selectable).each(function(){
              var item = $(this);
              if (item.attr('alt') == value) { item.addClass('ui-selected'); }
          });
      } else {
          var values = field.val().split(new RegExp(options.sep, 'g'));
          $('li', selectable).each(function(){
              var item = $(this);
              $(values).each(function(){
                  if (item.attr('alt') == this) { item.addClass('ui-selected'); }
              });
          });
      }
    }
    selectable.selectable({
        stop: function(){
          var selected = $(".ui-selected", this);
          if (!options.multiple && selected.length > 1) {
            selected.removeClass('ui-selected');
            initValue();
          } else {
            var value = new Array();
            selected.each(function(){value.push($(this).attr('alt'));});
            if (options.multiple)
                field.val(value.join(options.sep));
            else
                field.val(value.join(''));
          }
        }
    });
    initValue();
  },

  sortable: function(options) {
    var sep = options.sep;
    var field = $(document.getElementById(options.name));
    var sortable = $(document.getElementById(options.name+'_sortable'));
    sortable.sortable({
        stop: function(){
          var value = new Array();
          var sorted = $("li", this);
          sorted.each(function(){value.push($(this).text());});
          field.val(value.join(sep));
        }
    });
    sortable.disableSelection();
  },

  slider: function(field, plugin, options) {
    if (options.show_value) {
        var value = plugin.attr('id')+'_value';
        plugin.before('<label id="'+value+'">'+field.val()+'</label>');
        value = $('#'+value);
        $.extend(options, {
            slide: function(event, ui) {
              value.html(plugin.slider('value'));
            }
        });
    }
    $.extend(options, {
        value: parseInt(field.val()),
        stop:  function(event, ui) {
          field.val(plugin.slider('value'));
          if (options.show_value)
              value.html(plugin.slider('value'));
        }
    });
    plugin.slider(options);
  },

  colorpicker: function(options) {
    var field = $(document.getElementById(options.name));
    var picker = $(document.getElementById(options.name+'_colors'));
    var opts = options.options;
    $.extend(opts, { click: function(color) { field.val(color); } });
    picker.colorPicker(opts);
  }


});
})(jQuery);
