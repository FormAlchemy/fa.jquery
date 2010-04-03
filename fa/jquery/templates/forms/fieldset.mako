# -*- coding: utf-8 -*-
<%
from formalchemy import fatypes
_ = F_
_focus_rendered = False
%>\

%if fieldset.errors.get(None, []):
  <div class="ui-state-error ui-corner-all"><p>
    %for error in fieldset.errors.get(None, []):
      <div>
        ${_(error)}
      </div>
    %endfor
  </p></div>
%endif

%for field in fieldset.render_fields.itervalues():
  %if field.requires_label:
    <div class="fa_field ui-widget">
      <div class="label">
        %if isinstance(field.type, fatypes.Boolean):
          ${field.render()|n}
        %endif
        <label class="${field.is_required() and 'field_req' or 'field_opt'}" for="${field.renderer.name}">
          ${[field.label_text, fieldset.prettify(field.key)][int(field.label_text is None)]|h}
        </label>
      </div>
      %if 'instructions' in field.metadata:
      <div class="fa_instructions ui-corner-all">
        ${field.metadata['instructions']}
      </div>
      %endif
      %if field.errors:
        <div class="ui-state-error ui-corner-all">
        % for error in field.errors:
          <div>${_(error)}</div>
        % endfor
        </div>
      %endif
      %if not isinstance(field.type, fatypes.Boolean):
        <div>${field.render()|n}</div>
      %endif
    </div>
    %if (fieldset.focus == field or fieldset.focus is True) and not _focus_rendered:
      %if not field.is_readonly():
        <script type="text/javascript">
        //<![CDATA[
        document.getElementById("${field.renderer.name}").focus();
        //]]>
        </script>
        <% _focus_rendered = True %>\
      %endif
    %endif
  %else:
    ${field.render()}
  %endif
%endfor
