${html}
<script type="text/javascript">
  (function($) {
  var autocomplete = $(document.getElementById('${name}'));
  autocomplete.autocomplete(${data}${jq_options and ', ' + jq_options or ''});
  })(jQuery);
</script>
