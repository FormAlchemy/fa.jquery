<%!
from random import random
%>
<%
dom_id = 'grid_%s' % str(random())[2:]
fields = [field for field in collection.render_fields.values()]
%>
<table id="${dom_id}"></table> <div id="${dom_id}_jqgrid"></div> 
<script>
var url = window.location.href.split('?')[0] + '.json';
jQuery.fa.jqgrid("${dom_id}", {
    url: url+'?jqgrid=true',
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
