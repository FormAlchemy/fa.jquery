<div class="jGrowl" style="position:relative;">
%for id, theme, header, message in messages:
<div id="${id}" style="width:auto;display:none;" class="jGrowl-notification ui-state-highlight ui-corner-all ${theme}">
%if show_headers and header:
<div class="header">${header}</div>
%endif
${message}
</div>
%endfor
<script language="javascript">
jQuery(document).ready(function () {
%for id, life in lifes:
jQuery("#${id}").slideDown('slow', function() {
%if life:
var self = $(this);setTimeout(function() { self.slideUp('slow', function(){self.remove();}); }, ${life});
%endif
});
%endfor
});
</script>
</div>
