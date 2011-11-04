# -*- coding: utf-8 -*-
<%!
from formalchemy.ext.pylons.controller import model_url
from pylons import request
from fa.jquery.utils import url
%>
<%def name="h1(title, href=None)">
    <h1 class="ui-widget-header ui-corner-all">
      %if breadcrumb:
        <div class="breadcrumb">
         <a>/</a>${'<a>/</a>'.join(['<a href="%s">%s</a>' % (u or '',n.lower()) for u,n in breadcrumb])|n} 
        </div>
      %endif
      %if href:
        <a href="${href}">${title.title()}</a>
      %else:
        <a>${title.title()}</a>
      %endif
    </h1>
</%def>
<%def name="buttons()">
    <p class="fa_field">
      <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="#">
        <span class="ui-icon ui-icon-check"></span>
        Save
        <input type="submit" />
      </a>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url(collection_name)}">
        <span class="ui-icon ui-icon-circle-arrow-w"></span>
        Cancel
      </a>
    </p>
</%def>
<html>
  <head>
    <title>
    ${collection_name.title()}
    </title>
  </head>
  <body>
<div class="ui-admin ui-widget">
  %if isinstance(models, dict):
    <h1 class="ui-widget-header ui-corner-all"><a>Models</a></h1>
    %for name in sorted(models):
      <p>
        <a class="ui-state-default ui-corner-all" href="${models[name]}">${name}</a>
      </p>
    %endfor
  %elif is_grid:
    ${h1(model_name)}
    ${fs.render(template='jqgrid')}
  %else:
    ${h1(model_name, href=model_url(collection_name))}
    %if action == 'show':
      <table>
        ${fs.render()|n}
      </table>
      <p class="fa_field">
        <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url('edit_%s' % member_name, id=id)}">
          <span class="ui-icon ui-icon-pencil"></span>
          Edit
        </a>
      </p>
    %elif action == 'edit':
      <form action="${model_url(member_name, id=id)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        <input type="hidden" name="_method" value="PUT" />
        ${buttons()}
      </form>
    %else:
      <form action="${model_url(collection_name)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        ${buttons()}
      </form>
    %endif
  %endif
</div>
<script type="text/javascript">
  jQuery('a.ui-widget-button').click(function() {
    jQuery(this).parents('form').submit()
  });
</script>
</body></html>
