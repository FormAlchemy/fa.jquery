<div id="${id}_${rid}">
<ul>
%for fs in fieldsets:
<li><a href="#${fs['id']}_${rid}">${fs['title']}</a></li>
%endfor
</ul>
%for fs in fieldsets:
<div id="${fs['id']}_${rid}">
${header % fs}
${fs['fs'].render()}
${footer % fs}
</div>
%endfor
</div>
<script type="text/javascript">
  jQuery.fa.tabs('${id}_${rid}', ${options});
</script>
