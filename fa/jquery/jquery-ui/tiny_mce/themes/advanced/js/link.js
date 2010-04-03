tinyMCEPopup.requireLangPack();

var LinkDialog = {
	preInit : function() {
		var url;

		if (url = tinyMCEPopup.getParam("external_link_list_url"))
			document.write('<script language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></script>');
	},

	init : function() {
		var f = document.forms[0], ed = tinyMCEPopup.editor;

		// Setup browse button
		document.getElementById('hrefbrowsercontainer').innerHTML = getBrowserHTML('hrefbrowser', 'href', 'file', 'theme_advanced_link');
		if (isVisible('hrefbrowser'))
			document.getElementById('href').style.width = '180px';

		this.fillClassList('class_list');
		this.fillFileList('link_list', 'tinyMCELinkList');
		this.fillTargetList('target_list');

		if (e = ed.dom.getParent(ed.selection.getNode(), 'A')) {
			f.href.value = ed.dom.getAttrib(e, 'href');
			f.linktitle.value = ed.dom.getAttrib(e, 'title');
			f.insert.value = ed.getLang('update');
			selectByValue(f, 'link_list', f.href.value);
			selectByValue(f, 'target_list', ed.dom.getAttrib(e, 'target'));
			selectByValue(f, 'class_list', ed.dom.getAttrib(e, 'class'));
		}
// plupload stuff: dronnikov at gmail dot com, 2010-02-17
$('#hrefbrowser').each(function(event){
	//alert(0);
	var self = $(this);
	self.unbind('click');
	var uploader = new plupload.Uploader({
		// general settings
		runtimes: 'html5,flash',
		url: tinyMCEPopup.getParam('plupload_upload_url'), // || '/upload',
		max_file_size: tinyMCEPopup.getParam('plupload_upload_max_file_size') || '2mb',
		chunk_size: tinyMCEPopup.getParam('plupload_upload_chunk_size') || '1mb',
		/***************
		// resize images on clientside if we can
		resize: {width: 320, height: 240, quality: 90},
		// specify what files to browse for
		filters: [
			{title: 'Image files', extensions: 'jpg,gif,png'},
			{title: 'Zip files', extensions: 'zip'}
		],
		***************/
		// flash settings
		flash_swf_url: '../../../plupload/plupload.flash.swf',
		browse_button: 'hrefbrowser'
	});

	uploader.bind('PostInit', function() {
		//$('div.plupload_html5 >input[type=file]').click();
		//$(uploader).click();
	});

	uploader.bind('FilesAdded', function(up, files){
		$.each(files, function(i, file){
			$('#linktitle').val(file.name.replace(/\..+$/, ''));
		});
	});

	uploader.bind('UploadFile', function(up, file){
		// assign unique names
		file.target_name = (up.settings.salt||'') + file.id + '.tmp';
	});

	uploader.bind('QueueChanged', function(up){
		//window.console.info('CHANGED!');
		up.start();
	});

	uploader.bind('UploadProgress', function(up, file){
		$('#href').val(file.percent+'%');
		if (file.status == plupload.DONE)
			$('#href').val(up.settings.url + '/' + file.target_name);
		//window.console.log(file.id);
		//window.console.log(file.percent);
	});

	uploader.bind('FileUploaded', function(up, file){
		if (file.status == plupload.DONE) {
			//window.console.info('DONE');
			//window.console.log(file);
			$('#href').val(up.settings.url + '/' + file.target_name);
		} else if (file.status == plupload.FAILED) {
			// TODO: more friendly alert
			//window.console.info('FAILED');
			//window.console.log(up);
			//alert('Upload failed!');
		}
	});

	uploader.init();
});
// EO plupload stuff
	},

	update : function() {
		var f = document.forms[0], ed = tinyMCEPopup.editor, e, b;

		tinyMCEPopup.restoreSelection();
		e = ed.dom.getParent(ed.selection.getNode(), 'A');

		// Remove element if there is no href
		if (!f.href.value) {
			if (e) {
				tinyMCEPopup.execCommand("mceBeginUndoLevel");
				b = ed.selection.getBookmark();
				ed.dom.remove(e, 1);
				ed.selection.moveToBookmark(b);
				tinyMCEPopup.execCommand("mceEndUndoLevel");
				tinyMCEPopup.close();
				return;
			}
		}

		tinyMCEPopup.execCommand("mceBeginUndoLevel");

		// Create new anchor elements
		if (e == null) {
			ed.getDoc().execCommand("unlink", false, null);
			tinyMCEPopup.execCommand("CreateLink", false, "#mce_temp_url#", {skip_undo : 1});

			tinymce.each(ed.dom.select("a"), function(n) {
				if (ed.dom.getAttrib(n, 'href') == '#mce_temp_url#') {
					e = n;

					ed.dom.setAttribs(e, {
						href : f.href.value,
						title : f.linktitle.value,
						target : f.target_list ? getSelectValue(f, "target_list") : null,
						'class' : f.class_list ? getSelectValue(f, "class_list") : null
					});
				}
			});
		} else {
			ed.dom.setAttribs(e, {
				href : f.href.value,
				title : f.linktitle.value,
				target : f.target_list ? getSelectValue(f, "target_list") : null,
				'class' : f.class_list ? getSelectValue(f, "class_list") : null
			});
		}

		// Don't move caret if selection was image
		if (e.childNodes.length != 1 || e.firstChild.nodeName != 'IMG') {
			ed.focus();
			ed.selection.select(e);
			ed.selection.collapse(0);
			tinyMCEPopup.storeSelection();
		}

		tinyMCEPopup.execCommand("mceEndUndoLevel");
		tinyMCEPopup.close();
	},

	checkPrefix : function(n) {
		if (n.value && Validator.isEmail(n) && !/^\s*mailto:/i.test(n.value) && confirm(tinyMCEPopup.getLang('advanced_dlg.link_is_email')))
			n.value = 'mailto:' + n.value;

		if (/^\s*www\./i.test(n.value) && confirm(tinyMCEPopup.getLang('advanced_dlg.link_is_external')))
			n.value = 'http://' + n.value;
	},

	fillFileList : function(id, l) {
		var dom = tinyMCEPopup.dom, lst = dom.get(id), v, cl;

		l = window[l];

		if (l && l.length > 0) {
			lst.options[lst.options.length] = new Option('', '');

			tinymce.each(l, function(o) {
				lst.options[lst.options.length] = new Option(o[0], o[1]);
			});
		} else
			dom.remove(dom.getParent(id, 'tr'));
	},

	fillClassList : function(id) {
		var dom = tinyMCEPopup.dom, lst = dom.get(id), v, cl;

		if (v = tinyMCEPopup.getParam('theme_advanced_styles')) {
			cl = [];

			tinymce.each(v.split(';'), function(v) {
				var p = v.split('=');

				cl.push({'title' : p[0], 'class' : p[1]});
			});
		} else
			cl = tinyMCEPopup.editor.dom.getClasses();

		if (cl.length > 0) {
			lst.options[lst.options.length] = new Option(tinyMCEPopup.getLang('not_set'), '');

			tinymce.each(cl, function(o) {
				lst.options[lst.options.length] = new Option(o.title || o['class'], o['class']);
			});
		} else
			dom.remove(dom.getParent(id, 'tr'));
	},

	fillTargetList : function(id) {
		var dom = tinyMCEPopup.dom, lst = dom.get(id), v;

		lst.options[lst.options.length] = new Option(tinyMCEPopup.getLang('not_set'), '');
		lst.options[lst.options.length] = new Option(tinyMCEPopup.getLang('advanced_dlg.link_target_same'), '_self');
		lst.options[lst.options.length] = new Option(tinyMCEPopup.getLang('advanced_dlg.link_target_blank'), '_blank');

		if (v = tinyMCEPopup.getParam('theme_advanced_link_targets')) {
			tinymce.each(v.split(','), function(v) {
				v = v.split('=');
				lst.options[lst.options.length] = new Option(v[0], v[1]);
			});
		}
	}
};

LinkDialog.preInit();
tinyMCEPopup.onInit.add(LinkDialog.init, LinkDialog);
