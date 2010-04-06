(function($) {

$.fa.extend({
    jqgrid: function(table, pager, options) {
        var current_id;
        var base_url = window.location.href;
        var editRow = function(id) {
            if (id) {
                var edit_url = base_url+'/'+id+'.xhr?_method=PUT';
                var item_url = base_url+'/'+id+'/edit.xhr';
            } else {
                id = 'new';
                var edit_url = base_url+'.xhr';
                var item_url = base_url+'/new.xhr';
            }
            table.jqGrid('editGridRow', id, {
                url: edit_url,
                beforeShowForm: function(form) {
                    form.empty();
                    $('.navButton', form.parents('.ui-jqdialog')).remove();
                    form.load(item_url);
                },
                beforeSubmit: function(data, form) {
                    $(form.formToArray()).each(function() {
                        data[this.name] = $('#'+this.name).val();
                    });
                    return [true, 'saved'];
                },
                serializeEditData: function(data) {
                    // avoid PHP arrays
                    return $.param(data).replace(/%5B%5D=/g, '=');
                },
                afterComplete: function(response, postdata, form) {
                    if (id!='new') {
                        form.html(response.responseText);
                    } else {
                        if (/ui-state-error/.test(response.responseText))
                            form.html(response.responseText);
                        else
                            form.parents('.ui-jqdialog').jqmHide();
                    }
                }
            });
        }
        var settings = {
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
