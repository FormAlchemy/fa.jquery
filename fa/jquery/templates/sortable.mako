<input type="${show_input and 'text' or 'hidden'}" value="${value}" id="${name}" name="${name}" />
<ul id="${name}_sortable" class="fa_sortable">
%for k, v in tokens:
<li class="ui-state-default" alt="${v}"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>${k}</li>
%endfor
</ul>
<script type="text/javascript">
  jQuery.fa.sortable('${name}', {sep:'${sep}'});
</script>
