# -*- coding: utf-8 -*-
<%!
from pylons import url
%>
<textarea id="${name}" name="${name}" cols="120" rows="15">${value}</textarea>
<script type="text/javascript" src="${url('fa_static', path_info='tiny_mce/tiny_mce.js')}"></script>
<script type="text/javascript">
function richedit() {
## N.B: we want to just copy CSS from the current page!
var css = [];
$('link[rel=stylesheet]').each(function(){
	css.push($(this).attr('href'));
});
css = css.join(',');
// TODO: hackish!!!
// TODO: aint there a way to run it just once?!
tinyMCE.init({
	theme: 'advanced',
	mode: 'textareas',
	plugins: 'inlinepopups,advimage',
##	plugins: 'advimage',
	theme_advanced_buttons1: 'bold,italic,underline,undo,redo,link,unlink,image,forecolor,removeformat',
	theme_advanced_buttons2: '',
	theme_advanced_buttons3: '',
	theme_advanced_toolbar_location: 'bottom',
	theme_advanced_toolbar_align: 'center',
	theme_advanced_styles: 'Code=codeStyle;Quote=quoteStyle',
	content_css: css,
	entity_encoding: 'raw',
	add_unload_trigger: false,
	remove_linebreaks: false,
	inline_styles: false,
	convert_fonts_to_spans: true,
	theme_advanced_resizing: true,
	file_browser_callback: 'dummy-just-to-show-the-button',
	plupload_upload_url: '/upload',
	//plupload_upload_max_file_size: '2mb',
	//plupload_upload_chunk_size': '1mb',
	dialog_type: 'modal'
});
}
richedit();
</script>
