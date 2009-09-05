<input type="hidden" value="${value}" id="${name}" name="${name}" />
<div id="${name}_colors"></div>
<script type="text/javascript">
  (function($) {
    var field = $(document.getElementById('${name}'));
    var picker = $(document.getElementById('${name}_colors'));
    var opts = ${jq_options};
    $.extend(opts, { click: function(color) { field.val(color); } });
    picker.colorPicker(opts);
  })(jQuery);
</script>

