# -*- coding: utf-8 -*-
<%!
from pylons import url
%>
<%def name="buttons()">
    <p class="fa_field">
      <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="#">
        <span class="ui-icon ui-icon-check"></span>
        Save
        <input type="submit" />
      </a>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${url(collection)}">
        <span class="ui-icon ui-icon-circle-arrow-w"></span>
        Cancel
      </a>
    </p>
</%def>
<html>
  <head>
    <title>
    ${collection.title()}
    </title>
    <style type="text/css"><!-- @import url(${url('jquery', path_info='css/redmond/jquery-ui-1.7.2.custom.css')}); --></style>
    <style type="text/css"><!-- @import url(${url('jquery', path_info='fa.jquery.min.css')}); --></style>
    <style type="text/css">
      label {font-weight:bold;}
      h1, h3 {padding-left:0.5em;}
    </style>
    <script type="text/javascript" src="${url('jquery', path_info='fa.jquery.min.js')}"></script>
  </head>
  <body>
<div class="ui-admin ui-widget">
  %if is_grid:
    <h1 class="ui-widget-header ui-corner-all">${collection.title()} listing</h1>
    <div class="pager">
      ${page.pager()|n}
    </div>
    ${fs.render()|n}
    <p>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${url('new_%s' % member)}">
          <span class="ui-icon ui-icon-circle-plus"></span>
          New ${member}
      </a>
    </p>
  %else:
    <h1 class="ui-widget-header ui-corner-all"><a href="${url(collection)}">${collection.title()}</a></h1>
    %if action:
      %if id:
        <h3 class="ui-state-default ui-corner-all">Edit ${unicode(fs.model)}</h3>
        <form action="${action}" method="POST" enctype="multipart/form-data">
          ${fs.render()|n}
          <input type="hidden" name="_method" value="PUT" />
          ${buttons()}
        </form>
      %else:
        <h3 class="ui-state-default ui-corner-all">Add ${member}</h3>
        <form action="${action}" method="POST" enctype="multipart/form-data">
          ${fs.render()|n}
          ${buttons()}
        </form>
      %endif
    %else:
      <h3 class="ui-state-default ui-corner-all">${unicode(fs.model)}</h3>
      <table>
        ${fs.render()|n}
      </table>
      <p class="fa_field">
        <a class="ui-widget-header ui-widget-link ui-corner-all" href="${url('edit_%s' % member, id=id)}">
          <span class="ui-icon ui-icon-pencil"></span>
          Edit
        </a>
      </p>
    %endif
  %endif
</div>
<script type="text/javascript">
  jQuery('a.ui-widget-button').click(function() {jQuery('input', this).click(); return false;});
</script>
</body></html>
