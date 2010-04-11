(function($) {

$.fa.extend({
    jqgrid: function(table, pager, options) {
        var current_id;
        var base_url = window.location.href.split('?')[0];
        var editRow = function(id) {
            if (id) {
                var edit_url = base_url+'/'+id+'.xhr?_method=PUT';
                var item_url = base_url+'/'+id+'/edit.xhr';
                var form = $('<form title="Edit record"></form>');
            } else {
                id = 'new';
                var edit_url = base_url+'.xhr';
                var item_url = base_url+'/new.xhr';
                var form = $('<form title="New record"></form>');
            }
            pager.after(form);
            $.get(item_url, function(html) {
                form.append(html);
                form.dialog({
                    modal: true,
                    buttons: {
                        'Ok': function() {
                            var data = form.formToArray();
                            // avoid PHP arrays
                            data = $.param(data).replace(/%5B%5D=/g, '=');
                            $.post(edit_url, data, function(html) {
                                if (/ui-state-error/.test(html)) {
                                    form.empty();
                                    form.append(html);
                                } else {
                                    form.append(html);
                                    form.dialog('close');
                                    form.dialog('destroy');
                                    form.remove();
                                }
                                table.trigger('reloadGrid')
                            });
                        },
                        'Cancel': function() {
                                form.dialog('close');
                                form.dialog('destroy');
                                form.remove();
                        }
                    }
                });
                setTimeout(function() {
                    var text = $('textarea', form);
                    if (text.length) {
                        form.dialog('option', 'width', ''+(parseInt(text.css('width'))+50));
                        form.dialog('option', 'position', ['center','top']);
                    }
                }, 10);
            });
        }
        var settings = {
           url: base_url,
           datatype: "json",
           height: $(document).height()-200,
           width: $(document).width()-30,
           rowNum: parseInt(($(document).height()-200)/22),
           rowList:[10,20,50,100],
           pager: '#'+pager.attr('id'),
           sortname: 'id',
           viewrecords: true, sortorder: "desc",
           onCellSelect: function(id) { current_id = id },
           ondblClickRow:editRow
        }
        delete options['callback'];
        $.extend(settings, options);
        options['pager_id'] = '#'+pager.attr('id');
        table.jqGrid(settings)
        table.jqGrid('navGrid', options.pager_id,
                     {search:true}); 
        $('#add_'+table.attr('id'))
            .unbind('click')
            .click(function() { editRow(); });
        $('#edit_'+table.attr('id'))
            .unbind('click')
            .click(function() { editRow(current_id); });
        $('#del_'+table.attr('id'))
            .unbind('click')
            .click(function() {
                table.jqGrid('delGridRow', current_id,
                             {url:base_url+'/'+current_id+'.json?_method=DELETE'});
            });
    }
});

})(jQuery);
