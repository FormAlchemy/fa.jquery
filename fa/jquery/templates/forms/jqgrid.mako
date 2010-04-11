<%!
from random import random
from fa.jquery.utils import url
%>
<%
dom_id = 'grid_%s' % str(random())[2:]
fields = [field for field in collection.render_fields.values()]
%>
<table id="${dom_id}"></table> <div id="${dom_id}_jqgrid"></div> 
<script>
jQuery.fa.add_resource(${repr(url('jqgrid/css/ui.jqgrid.css'))});
jQuery.fa.add_resource(${repr(url('jqgrid/js/i18n/grid.locale-en.js'))});
jQuery.fa.add_resource(${repr(url('jqgrid/js/jquery.jqGrid.min.js'))});
jQuery.fa.add_resource(${repr(url('jqgrid/js/fa.jqgrid.js'))});
</script>
<script>
jQuery.fa.jqgrid("${dom_id}", {
    url: window.location.href.split('?')[0]+'.json?jqgrid=true',
    colNames:['id'
      %for field in fields:
      ,"${field.label_text or collection.prettify(field.key)}"
      %endfor
    ],
    colModel:[
      {name:"id",index:"id", width:30, align:"center", searchoptions:{sopt:["eq"]}}
      %for field in fields:
      ,{name:"${field.key}",index:"${field.key}",
        sortable:${field.metadata.get('sortable', field.is_relation and 'false' or 'true')}
        %for k in ('width', 'align', 'fixed', 'search', 'stype', 'searchoptions'):
          %if k in field.metadata:
            ,${k}: ${field.metadata[k]}
          %endif
        %endfor
       }
      %endfor
    ],
    callback: function(table, pager, options) {
    }
  });
</script>
