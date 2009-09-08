jQuery.extend({fa:{}});
jQuery.extend(jQuery.fa, {
  selectable: function(options) {
    var sep = options.sep;
    var field = $(document.getElementById(options.name));
    var selectable = $(document.getElementById(options.name+'_selectable'));
    var error = $(document.getElementById(options.name+'_error'));
    var initValue = function() {
      var value = field.val();
      $('li', selectable).each(function(){
          var item = $(this);
          if (item.attr('alt') == value) { item.addClass('ui-selected'); }
      });
    }
    selectable.selectable({
        stop: function(){
          var selected = $(".ui-selected", this);
          if (options.multiple && selected.length > 1) {
            selected.removeClass('ui-selected');
            initValue();
            dialog = error.clone();
            dialog.dialog({height: 140,modal: true});
          } else {
            selected.each(function(){val=val+$(this).text()+sep;});
            field.val(val.substring(0, val.length-1));
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
          var val = '';
          var sorted = $("li", this);
          sorted.each(function(){val=val+$(this).text()+sep;});
          field.val(val.substring(0, val.length-1));
        }
    });
    sortable.disableSelection();
  },

  slider: function(options) {
    var field = $(document.getElementById(options.name));
    var slider = $(document.getElementById(options.name+'_slider'));
    slider.slider({
        value: 0,
        stop:  function(event, ui) {
          field.val(slider.slider('value'));
        }
    });
  },

  colorpicker: function(options) {
    var field = $(document.getElementById(options.name));
    var picker = $(document.getElementById(options.name+'_colors'));
    var opts = options.options;
    $.extend(opts, { click: function(color) { field.val(color); } });
    picker.colorPicker(opts);
  }


});
