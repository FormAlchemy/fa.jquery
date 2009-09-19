<div id="${id}">
<ul>
%for fs in fieldsets:
<li><a href="#${fs['id']}">${fs['title']}</a></li>
%endfor
</ul>
%for fs in fieldsets:
<div id="${fs['id']}">
${header % fs}
${fs['fs'].render()}
${footer % fs}
</div>
%endfor
</div>
<script type="text/javascript">
  jQuery.fa.tabs('${id}', ${options});
</script>
