(function($) {

$.fa.extend({
    jqgrid: function(table, pager, options) {
        var current_id;
        var base_url = window.location.href.split('?')[0];
        var editRow = function(id) {
            var subpath = '/';
            if (id) {
                var item_url = base_url+subpath+id+'/edit';
            } else {
                var item_url = base_url+subpath+'new';
            }
            window.location.href = item_url;
        }
        var settings = {
           url: base_url,
           datatype: "json",
           height: $(document).height()-200,
           width: $('#content').width()-30,
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
                             {url:base_url+'/json/'+current_id+'/delete'});
            });
    }
});

})(jQuery);
