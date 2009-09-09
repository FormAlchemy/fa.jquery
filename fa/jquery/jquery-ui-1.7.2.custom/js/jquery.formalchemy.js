jQuery.extend({fa:{}});
jQuery.extend(jQuery.fa, {
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
            dialog = error.clone();
            dialog.dialog({height: 140,modal: true});
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

  slider: function(options) {
    var field = $(document.getElementById(options.name));
    var slider = $(document.getElementById(options.name+'_slider'));
    slider.slider({
        value: parseInt(field.val()),
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
