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
  },
/**
 * jQuery plugin to help dealing with UI dialogs
 * Copyright (c) 2010, Vladimir Dronnikov, dronnikov@gmail.com
 * Licensed under the MIT license
 * http://www.opensource.org/licenses/mit-license.php
 * Date: 2010-01-29
 *
 * Depends on: jquery.form
 *
 * Usage: jQuery.ajaxDialog({options});
 *
 * I18n: options.applyText -- text for Apply button
 *       options.closeText -- text for Close button
 *
 */
	ajaxDialog: function(options){
		var div;
		// patch options
		options = $.extend({
			id: 'dialog', // default placeholder id
			modal: true,
			//bgiframe: true, // use IE6 select workaround? No, let the sucker die!
			autoOpen: false,
			width: 500,
			//show: 'transfer', // UI effect on show
			//hide: 'explode', // UI effect on hide
			//zIndex: 1000, // TODO: make datepicker of higher zIndex! Or datepicker is hidden by dialog
			title: 'Dialog'
		}, options || {});
		// append buttons. N.B. this pervert method is due to buttons hash keys are texts of buttons.
		// So buttons = {options.closeText: function...} doesn't work
		options.buttons = {};
		options.buttons[options.closeText || 'Close'] = function(){
			$(this).dialog('close');
		};
		options.buttons[options.applyText || 'Apply'] = function(){
			var form = $('form', this);
			// on asyncronous submit reload the dialog
			$('form', this).ajaxSubmit(function(text){
				// empty result means OK, close the dialog
				if ('' === text) {
					div.dialog('close');
					try{reloadPage();}catch(x){}
				} else {
					div.html(text);
				}
			});
			return false;
		};
		// insert placeholder
		$('body').append('<div id="'+options.id+'">'+(options.content||'')+'</div>');
		div = $('#'+options.id);
		// init dialog
		div.dialog(options);
		// setup background dimming
		$('div.ui-widget-overlay').css({
			'background': '#666666 url(images/ui-bg_diagonals-thick_18_b81900_40x40.png) repeat scroll 50% 50%;',
			'opacity': '0.5'
		});
		// make anchors classed .load-dialog load href-ered content to this dialog
		$('a.load-dialog').live('click', function(){
			div.load($(this).attr('href'), function(text){
				div.dialog('open');
			});
			/*
			var a = $(this);
			var data = undefined;
			// first check confirmation
			if (a.hasClass('confirm-operation'))
				$.confirm();
			// set request method
			if (a.hasClass('method-delete'))
				data = {_method: 'DELETE'};
			div.load($(this).attr('href'), data, function(text){
				div.dialog('open');
			});
			*/
			return false;
		});
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
