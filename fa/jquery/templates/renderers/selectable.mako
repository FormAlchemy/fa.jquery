<input type="hidden" value="${value}" id="${name}" name="${name}" />
<ul id="${name}_selectable" class="fa_selectable">
%for k, v in options:
<li class="ui-widget-content" alt="${v}">${k}</li>
%endfor
</ul>
<script type="text/javascript">
  jQuery.fa.selectable('${name}', ${jq_options});
</script>
