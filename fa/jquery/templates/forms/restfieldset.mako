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
    %if 'debug' in request.GET:
    <link type="text/css" href="/jquery/css/redmond/jquery-ui-1.8.custom.css" rel="stylesheet" />
    <link type="text/css" href="/jquery/colorpicker/syronex-colorpicker.css" rel="stylesheet" />
    <link type="text/css" href="/jquery/css/jquery.jgrowl.css" rel="stylesheet" />
    <link type="text/css" href="/jquery/fa/jquery.formalchemy.css" rel="stylesheet" />

    <script type="text/javascript" src="/jquery/js/jquery-1.4.2.min.js"></script>
    <script type="text/javascript" src="/jquery/js/jquery-ui-1.8.custom.min.js"></script>
    <script type="text/javascript" src="/jquery/colorpicker/syronex-colorpicker.js"></script>
    <script type="text/javascript" src="/jquery/js/jquery.jgrowl_minimized.js"></script>
    <script type="text/javascript" src="/jquery/js/jquery.form.js"></script>
    <script type="text/javascript" src="/jquery/fa/jquery.formalchemy.js"></script>
    %else:
    <link type="text/css" rel="stylesheet" href="${url('css/redmond/jquery-ui-1.8.custom.css')}" />
    <link type="text/css" rel="stylesheet" href="${url('fa.jquery.min.css')}" />
    <script type="text/javascript" src="${url('fa.jquery.min.js')}"></script>
    %endif
    <style type="text/css">
      label {font-weight:bold;}
      h1, h3 {padding:0.1 0.3em;}
      h1 a, h3 a {text-decoration:none;}
      a.ui-state-default {padding:0.1em 0.3em;}
      a.fm-button {padding:0.4em 0.5em;}
      a.fm-button-icon-left {padding-left:1.9em;}
      div.breadcrumb {float:right; font-size:0.7em;}
      div.breadcrumb a {text-decoration:underline}
    </style>
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
  jQuery('a.ui-widget-button').click(function() {jQuery('input', this).click(); return false;});
</script>
</body></html>
