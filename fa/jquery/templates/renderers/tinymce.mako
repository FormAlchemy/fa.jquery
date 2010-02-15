# -*- coding: utf-8 -*-
<%!
from pylons import url
%>
<textarea id="${name}" name="${name}" cols="120" rows="15" class="mceAdvanced">${value}</textarea>
<script type="text/javascript" src="${url('fa_static', path_info='tiny_mce/tiny_mce.js')}"></script>
<script type="text/javascript">
function richedit() {
var css = [];
$('link[rel=stylesheet]').each(function(){
	css.push($(this).attr('href'));
});
css = css.join(',');
//console.log(css);
// TODO: hackish!!!
tinyMCE.init({
##	editor_selector: 'mceAdvanced',
	theme: 'advanced',
	mode: 'textareas',
	plugins: 'advimage',
	theme_advanced_buttons1: 'bold,italic,underline,undo,redo,link,unlink,image,forecolor,removeformat',
	theme_advanced_buttons2: '',
	theme_advanced_buttons3: '',
	theme_advanced_toolbar_location: 'bottom',
	theme_advanced_toolbar_align: 'center',
	theme_advanced_styles: 'Code=codeStyle;Quote=quoteStyle',
## TODO: how to just copy CSS from the current page?!
##	content_css: "${url('fa_static', path_info='css/ui-lightness/jquery-ui-1.8rc1.custom.css')},${url('fa_static', path_info='fa.jquery.min.css')}",
	content_css: css,
	entity_encoding: 'raw',
	add_unload_trigger: false,
	remove_linebreaks: false,
	inline_styles: false,
	convert_fonts_to_spans: true,
	theme_advanced_resizing: true,
});
}
richedit();
</script>
