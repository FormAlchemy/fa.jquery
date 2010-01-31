<%!
from pylons import url
from simplejson import dumps
%>
<textarea id="${name}" name="${name}">${value}</textarea>
<link type="text/css" rel="stylesheet" href="${url('fa_static', path_info='markitup/skins/simple/style.css')}" />
<link type="text/css" rel="stylesheet" href="${url('fa_static', path_info='markitup/sets/'+markup+'/style.css')}" />
<script type="text/javascript" src="${url('fa_static', path_info='markitup/sets/'+markup+'/set.js')}"></script>
<script type="text/javascript">
##	jQuery.fa.markitup('${name}', ${dumps(jq_options.update(previewTemplatePath=url('fa_static', path_info='markitup/templates/preview.html')))});
	jQuery.fa.markitup('${name}', ${jq_options});
</script>

