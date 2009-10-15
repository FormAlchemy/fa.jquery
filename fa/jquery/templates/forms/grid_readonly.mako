# -*- coding: utf-8 -*-
<thead>
  <tr class="ui-widget-header">
    %for field in collection.render_fields.itervalues():
      <th>${field.label_text or collection.prettify(field.key)|h}</th>
    %endfor
  </tr>
</thead>

<tbody>
%for i, row in enumerate(collection.rows):
  <% collection._set_active(row) %>
  <tr class="${i % 2 and 'ui-widget-odd' or 'ui-widget-even'}">
  %for field in collection.render_fields.itervalues():
    <td class="normal">${field.render_readonly()|n}</td>
  %endfor
  </tr>
%endfor
</tbody>
