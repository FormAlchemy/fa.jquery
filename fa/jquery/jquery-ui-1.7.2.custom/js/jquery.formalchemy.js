(function($) {

var log = function(message) {
    try { window.console.log(message); } catch (e) {};
}

var pluginGen = function(plugin_id, func) {
    return function(name, options) {
        // assume plugin is launch onload
        $(function(){
            try {
                var field = $(document.getElementById(name));
                var plugin = document.getElementById(name+'_'+plugin_id);
                if (plugin)
                    plugin = $(plugin);
                $.fa_plugins[plugin_id](field, plugin, options);
            } catch (e) {
                log('Error while loading '+plugin_id+' for '+name+' - '+options+': '+e);
            }
        });
    }
}

$.extend({
  fa_plugins:{},
  fa: {
      extend: function(plugins) {
        for (k in plugins) {
            $.extend($.fa_plugins, plugins);
            $.fa[k] = pluginGen(k, plugins[k]);
        }
  }
}});

$.fa.extend({
  datepicker: function(field, plugin, options) {
    field.datepicker(options);
  },
  autocomplete: function(field, plugin, options) {
    plugin.remove();
    var data = options.data;
    delete options.data;
    field.autocomplete(data, options);
  },
  selectable: function(field, plugin, options) {
    var error = $(document.getElementById(options.name+'_error'));
    var initValue = function() {
      if (!options.multiple) {
          var value = field.val();
          $('li', plugin).each(function(){
              var item = $(this);
              if (item.attr('alt') == value) { item.addClass('ui-selected'); }
          });
      } else {
          var values = field.val().split(new RegExp(options.sep, 'g'));
          $('li', plugin).each(function(){
              var item = $(this);
              $(values).each(function(){
                  if (item.attr('alt') == this) { item.addClass('ui-selected'); }
              });
          });
      }
    }
    plugin.selectable({
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

  sortable: function(field, plugin, options) {
    var sep = options.sep;
    var sortable = plugin;
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

  colorpicker: function(field, plugin, options) {
    $.extend(options, {
        click: function(color) { field.val(color); },
        defaultColor: field.val()
    });
    plugin.colorPicker(options);
  },
  tabs: function(field, plugin, options) {field.tabs(options);}

});


})(jQuery);
