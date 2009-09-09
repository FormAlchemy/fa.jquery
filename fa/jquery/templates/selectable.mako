<input type="hidden" value="${value}" id="${name}" name="${name}" />
<div id="${name}_error" title="Error" style="display:none">
  <p>You can only select one value</p>
</div>
<ul id="${name}_selectable" class="fa_selectable">
%for k, v in options:
<li class="ui-widget-content" alt="${v}">${k}</li>
%endfor
</ul>
<script type="text/javascript">
  jQuery.fa.selectable(${jq_options});
</script>
