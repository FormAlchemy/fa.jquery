<div id="${id}">
<ul>
%for form in forms:
<li><a href="#${form['id']}">${form['title']}</a></li>
%endfor
</ul>
%for form in forms:
<div id="${form['id']}">
${header % form}
${form['fs'].render()}
${footer % form}
</div>
%endfor
</div>
<script type="text/javascript">
  jQuery('#${id}').tabs(${options});
</script>
