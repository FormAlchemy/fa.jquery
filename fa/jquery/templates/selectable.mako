<input type="hidden" value="${value}" id="${name}" name="${name}" />
<div id="${name}_error" title="Error" style="display:none">
  <p>You can only select one value</p>
</div>
<ul id="${name}_selectable" class="selectable">
%for k, v in options:
<li alt="${v}">${k}</li>
%endfor
</ul>
<script type="text/javascript">
  (function($) {
    var field = $(document.getElementById('${name}'));
    var selectable = $(document.getElementById('${name}_selectable'));
    var error = $(document.getElementById('${name}_error'));
    selectable.selectable({
        stop: function(){
          var selected = $(".ui-selected", this);
          if (selected.length > 1) {
            dialog = error.clone();
            dialog.dialog({height: 140,modal: true});
          } else {
            selected.each(function(){field.val($(this).attr('alt'));});
          }
        }
    });
    var value = field.val();
    $('li', selectable).each(function(){
        var item = $(this);
        if (item.attr('alt') == value) { item.addClass('ui-selected'); }
    });
  })(jQuery);
</script>
