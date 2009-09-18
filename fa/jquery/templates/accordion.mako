<div id="${id}">
%for fs in fieldsets:
<h3><a href="#${fs['id']}">${fs['title']}</a></h3>
<div id="${fs['id']}">
${header % fs}
${fs['fs'].render()}
${footer % fs}
</div>
%endfor
</div>
<script type="text/javascript">
  jQuery.fa.accordion('${id}', ${options});
</script>
