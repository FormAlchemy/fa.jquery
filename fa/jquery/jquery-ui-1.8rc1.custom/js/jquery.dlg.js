
  var griddialog = function(options) {
    // insert placeholder
    $('body').append('<div id="form"></div>');
    var plugin = $('#form');
    // patch options
    options = $.extend(options || {}, {
        modal: true,
        //bgiframe: true, // IE6 select workaround
        autoOpen: false,
        width: 500,
        //show: 'transfer', // UI effect on show
        //hide: 'explode', // UI effect on hide
        title: 'Dialog', // TODO: i18n
        //zIndex: 1000, // TODO: make datepicker of higher zIndex! Or datepicker is hidden by dialog
        buttons: {
            'Close': function(){ // TODO: i18n
                $(this).dialog('close');
            },
            'Apply': function(){ // TODO: i18n
                $('form', this).ajaxSubmit(function(text){
					plugin.html(text);
				});
				return false;
            }
        }
    });
    // init dialog
    plugin.dialog(options);
    // setup background dimming
    $('div.ui-widget-overlay').css({
        'background': '#444444 url(images/ui-bg_diagonals-thick_20_666666_40x40.png) repeat scroll 50% 50%;',
        'opacity': '0.5'
    });
  };
