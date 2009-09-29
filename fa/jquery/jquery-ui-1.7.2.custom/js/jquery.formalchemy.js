(function($) {

var log = function(message) {
    try { window.console.log(message); } catch (e) {};
}

$.fn.extend({
    getFaField: function(name) {
        var id = $(this).attr('id').split('-', 2).join('-');
        var field = document.getElementById(id+'-'+name);
        return $(field);
    }
});


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
  fa_resources:[],
  fa: {
      extend: function(plugins) {
        for (k in plugins) {
            $.extend($.fa_plugins, plugins);
            $.fa[k] = pluginGen(k, plugins[k]);
        }
      },
      add_resource: function(url) {
        if (!url || $.fa_resources.indexOf(url) > -1)
            return;
        $.fa_resources.push(url);
        var head = document.getElementsByTagName("head")[0] || document.documentElement;
        if (/\.js$/.test(url)) {
            if ($.browser.safari) {
                document.write('<scr'+'ipt type="text\/javascr'+'ipt" src="'+url+'"><\/scr'+'ipt>');
            } else {
                var obj = document.createElement("script");
                obj.type= 'text/javascript';
                obj.src = url;
                head.insertBefore(obj, head.firstChild);
            }
        } else if (/\.css$/.test(url)) {
            var obj = document.createElement("link");
            obj.type = 'text/css';
            obj.rel = 'stylesheet';
            obj.href = url;
            head.insertBefore(obj, head.firstChild);
        } else {
            log('Invalid resource url: '+url);
        }
     }
  },
  getFaField: function(name) {
      field = $('input[id$="'+name+'"]');
      if (field.length == 1)
          return field;
  }
});

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
        var widget = $(plugin.parents('div.fa_field')[0])
        $('div.label', widget).append('<label id="'+value+'">'+field.val()+'</label>');
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
  tabs: function(field, plugin, options) {field.tabs(options);},
  accordion: function(field, plugin, options) {field.accordion(options);}

});


})(jQuery);
