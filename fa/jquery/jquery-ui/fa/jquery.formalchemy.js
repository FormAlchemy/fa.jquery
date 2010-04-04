
var markitup_settings = {};

if (!Array.indexOf) {
  // Old IE do not support indexOf
  Array.prototype.indexOf = function (obj, start) {
    for (var i = (start || 0); i < this.length; i++) {
      if (this[i] == obj) {
        return i;
      }
    }
    return -1;
  }
}

(function($) {

var log = function(message) {
    try { window.console1.log(message); } catch (e) {}
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
  fa_resources:new Array(),
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
            if ($.browser.safari || $.browser.msie) {
                document.write(unescape('%3Cscr'+'ipt type="text/javascr'+'ipt" src="'+url+'"%3E%3C/scr'+'ipt%3E'));
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
    field.autocomplete(options);
  },
  selectable: function(field, plugin, options) {
    var ui = $('<ul class="fa_selectable"></ul>');
    plugin.append(ui);
    $('option', field).each(function(){
        var opt = $(this);
        var ui_opt = ui.append('<li class="ui-widget-content" '+
                  'alt="'+opt.attr('value')+'">'+opt.text()+'</li>');
    });
    var initValue = function() {
      var selected = $(".ui-selected", ui);
      selected.removeClass('ui-selected');
      if (!options.multiple) {
          $('li[alt="'+field.val()+'"]', ui).addClass('ui-selected');
      } else {
          $(field.val()).each(function(){
            $('li[alt="'+this+'"]', ui).addClass('ui-selected');
          });
      }
    }
    ui.selectable({
        stop: function(){
          var selected = $(".ui-selected", this);
          if (!options.multiple && selected.length > 1) {
            initValue();
          } else {
            var value = new Array();
            selected.each(function(){value.push($(this).attr('alt'));});
            if (options.multiple)
                field.val(value);
            else
                field.val(value);
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
  accordion: function(field, plugin, options) {field.accordion(options);},
  markitup: function(field, plugin, options) {
      plugin.remove();
      var nameSpace = options['nameSpace'];
      field.markItUp($.extend(markitup_settings[nameSpace], options));
  },
  tinymce: function(field, plugin, options) {
        plugin.remove();
        if (!options.width)
            field.css('width','100%');
        if (!options.height)
            field.css('height','20em');
        field.tinymce(options);
  }

});


})(jQuery);
