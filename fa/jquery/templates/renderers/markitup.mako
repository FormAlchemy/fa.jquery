# -*- coding: utf-8 -*-
<%!
from pylons import url
%>
## editor area
<textarea id="${name}" name="${name}">${value}</textarea>
## inline upload form
<link type="text/css" rel="stylesheet" href="${url('fa_static', path_info='markitup/sets/'+markup+'/style.css')}" />
<script type="text/javascript" src="${url('fa_static', path_info='markitup/sets/'+markup+'/set.js')}"></script>
<script type="text/javascript">
// attach markItUp! editor
jQuery('#${name}}').markItUp($.extend(mySettings, {
}));
</script>
