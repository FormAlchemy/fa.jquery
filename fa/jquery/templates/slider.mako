<input type="hidden" value="${value}" id="${name}" name="${name}" />
<div id="${name}_slider"></div>
<script type="text/javascript">
  (function($) {
  var field = $(document.getElementById('${name}'));
  var slider = $(document.getElementById('${name}_slider'));
  slider.slider({
      value: ${value},
      stop:  function(event, ui) {
        field.val(slider.slider('value'));
      }
      });
  })(jQuery);
</script>

