# -*- coding: utf-8 -*-
import os
from formalchemy import helpers as h
from formalchemy import types
from formalchemy import fields
from formalchemy import config
from mako.lookup import TemplateLookup

dirname = os.path.join(os.path.dirname(__file__), 'templates')
templates = TemplateLookup([dirname], input_encoding='utf-8', output_encoding='utf-8')

class TextFieldRenderer(fields.TextFieldRenderer):
    pass

class DateFieldRenderer(fields.DateFieldRenderer):
    """Use http://jqueryui.com/demos/datepicker/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.date.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="text" size="10" value="" id="Sample--date" name="Sample--date" />
        <script type="text/javascript">
          jQuery(document.getElementById('Sample--date')).datepicker({dateFormat:'yy-mm-dd'});
        </script>...
        
    """
    template = templates.get_template('date.mako')
    jq_options = "{dateFormat:'yy-mm-dd'}"
    def render(self, **kwargs):
        value = self._value or ''
        value = value and value.split()[0] or ''
        kwargs.update(
            name=self.name,
            value=value,
            jq_options=self.jq_options,
        )
        return self.template.render(**kwargs)

    def _serialized_value(self):
        value = self._params.getone(self.name) or ''
        return value

class DateTimeFieldRenderer(DateFieldRenderer, fields.TimeFieldRenderer):
    """Use http://jqueryui.com/demos/datepicker/"""
    format = '%Y-%m-%d %H:%M:%S'
    template = templates.get_template('date.mako')
    jq_options = "{dateFormat:'yy-mm-dd'}"
    def render(self, **kwargs):
        return h.content_tag('span', DateFieldRenderer.render(self, **kwargs) + ' ' + fields.TimeFieldRenderer._render(self, **kwargs))

    def _serialized_value(self):
        return DateFieldRenderer._serialized_value(self) + ' ' + fields.TimeFieldRenderer._serialized_value(self)

class SliderFieldRenderer(fields.IntegerFieldRenderer):
    """Fill an integer field using http://jqueryui.com/demos/slider/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.slider.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="0" id="Sample--slider" name="Sample--slider" />
        <div id="Sample--slider_slider"></div>
        <script type="text/javascript">
          (function($) {
          var field = $(document.getElementById('Sample--slider'));
          var slider = $(document.getElementById('Sample--slider_slider'));
          slider.slider({
              value: 0,
              stop:  function(event, ui) {
                field.val(slider.slider('value'));
              }
              });
          })(jQuery);
        </script>...
    """
    template = templates.get_template('slider.mako')
    def render(self, **kwargs):
        value = self._value or 0
        return self.template.render(name=self.name, value=value)

class SelectableFieldRenderer(fields.SelectFieldRenderer):
    """Fill a text field using http://jqueryui.com/demos/selectable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.selectable.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="" id="Sample--selectable" name="Sample--selectable" />
        <div id="Sample--selectable_error" title="Error" style="display:none">
          <p>You can only select one value</p>
        </div>
        <ul id="Sample--selectable_selectable" class="selectable">
        <li alt="a">a</li>
        <li alt="b">b</li>
        <li alt="c">c</li>
        <li alt="d">d</li>
        <li alt="e">e</li>
        <li alt="f">f</li>
        </ul>
        <script type="text/javascript">
          (function($) {
            var field = $(document.getElementById('Sample--selectable'));
            var selectable = $(document.getElementById('Sample--selectable_selectable'));
            var error = $(document.getElementById('Sample--selectable_error'));
            selectable.selectable({
                stop: function(){
                  var selected = $(".ui-selected", this);
                  if (selected.length > 1) {
                    dialog = error.clone();
                    dialog.dialog({height: 140,modal: true});
                  } else {
                    selected.each(function(){field.val($(this).attr('alt'));});
                  }
                }
            });
            var value = field.val();
            $('li', selectable).each(function(){
                var item = $(this);
                if (item.attr('alt') == value) { item.addClass('ui-selected'); }
            });
          })(jQuery);
        </script>...

    """
    template = templates.get_template('selectable.mako')
    def render(self, options, **kwargs):
        value = self._value or ''
        if callable(options):
            L = fields._normalized_options(options(self.field.parent))
            if not self.field.is_required() and not self.field.is_collection:
                L.insert(0, self.field._null_option)
        else:
            L = list(options)
        if len(L) > 0:
            if len(L[0]) == 2:
                L = [(k, self.stringify_value(v)) for k, v in L]
            else:
                L = [fields._stringify(k) for k in L]
                L = [(k, k) for k in L]
        return self.template.render(name=self.name, value=value, options=L)


default_renderers = {
    types.Date:DateFieldRenderer,
    types.DateTime:DateTimeFieldRenderer,
}
