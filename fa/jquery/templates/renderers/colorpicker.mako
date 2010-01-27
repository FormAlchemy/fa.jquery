<input type="${show_input and 'text' or 'hidden'}" value="${value}" id="${name}" name="${name}" />
<div id="${name}_colors"></div>
<script type="text/javascript">
  jQuery.fa.colorpicker({name:'${name}', options:${jq_options}});
</script>
