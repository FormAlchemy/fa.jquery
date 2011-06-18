<div id="${id}_${rid}">
%for fs in fieldsets:
<fieldset id="${fs['id']}_${rid}">
%if fs['title']:
<legend><a href="#${fs['id']}_${rid}">${fs['title']}</a></legend>
%endif
<div>
${header % fs}
${fs['fs'].render()}
${footer % fs}
</div>
</fieldset>
%endfor
</div>
