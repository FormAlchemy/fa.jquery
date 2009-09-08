# -*- coding: utf-8 -*-
import os
from simplejson import dumps
from formalchemy import helpers as h
from formalchemy import types
from formalchemy import fields
from formalchemy import config

from utils import templates

def jQueryFieldRenderer(plugin, show_input=False, tag='div', renderer=fields.TextFieldRenderer, **jq_options):
    """Extending jQuery.fa:

    .. sourcecode:: python

        >>> from testing import fs
        >>> renderer = jQueryFieldRenderer('myplugin', option1=True, option2=['a', 'b'])
        >>> field = fs.title.set(renderer=renderer)
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><input id="Sample--title" name="Sample--title" type="text" /></div>
        <div id="Sample--title_myplugin"></div>
        <script type="text/javascript">
          jQuery.fa.myplugin(jQuery(document.getElementById('Sample--title')),
                             jQuery(document.getElementById('Sample--title_myplugin')),
                             {"option2": ["a", "b"], "option1": true});
        </script>...
        
    Then in your javascript code:

    .. sourcecode:: javascript

        jQuery.extend(jQuery.fa, {
            myplugin: function(field, plugin, options) {
                // do what you want
           }
       });

    """
    class Renderer(renderer):
        template=templates.get_template('jquery.mako')
        def render(self, **kwargs):
            html = renderer.render(self, **kwargs)
            kwargs.update(jq_options)
            options = dict(
                tag=tag,
                html=html,
                plugin=plugin,
                name=self.name,
                show_input=show_input,
                options=dumps(kwargs)
            )
            return self.template.render(**options)
    return Renderer

plugin = jQueryFieldRenderer

def AutoCompleteFieldRenderer(url_or_data, renderer=fields.TextFieldRenderer, **jq_options):
    """Use http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.title.set(renderer=AutoCompleteFieldRenderer(['aa', 'bb']))
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input id="Sample--title" name="Sample--title" type="text" />
        <script type="text/javascript">
          (function($) {
          var autocomplete = $(document.getElementById('Sample--title'));
          autocomplete.autocomplete(["aa", "bb"]);
          })(jQuery);
        </script>

    With more advanced options:

    .. sourcecode:: python

        >>> field = fs.title.set(
        ...     renderer=AutoCompleteFieldRenderer(
        ...         ['aa', 'bb'],
        ...         width=320,
        ...         scroll=True,
        ...         scrollHeight=300, 
        ...         ))
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input id="Sample--title" name="Sample--title" type="text" />
        <script type="text/javascript">
          (function($) {
          var autocomplete = $(document.getElementById('Sample--title'));
          autocomplete.autocomplete(["aa", "bb"], {"width": 320, "scroll": true, "scrollHeight": 300});
          })(jQuery);
        </script>
            
    """
    class Renderer(renderer):
        template=templates.get_template('autocomplete.mako')
        def render(self, options=None, **kwargs):
            html = renderer.render(self, **kwargs)
            data = url_or_data or options or []
            kwargs.update(
                html=html,
                name=self.name,
                data=dumps(data),
                jq_options=jq_options and dumps(jq_options) or '',
            )
            return self.template.render(**kwargs)
    return Renderer

autocomplete = AutoCompleteFieldRenderer

def SortableTextFieldRenderer(sep=';', show_input=False, **jq_options):
    class Renderer(fields.TextFieldRenderer):
        template=templates.get_template('sortable.mako')
        def render_readonly(self):
            return ', '.join(self._value.split(sep))
        def render(self, **kwargs):
            value=self._value.strip(sep)
            tokens = value and value.split(sep) or ''
            tokens = [(v, v) for v in tokens]
            kwargs.update(
                name=self.name,
                sep=sep,
                value=value,
                tokens=tokens,
                show_input=show_input,
                jq_options=dumps(jq_options),
            )
            return self.template.render(**kwargs)
    return Renderer

sortable_text = SortableTextFieldRenderer

def ColorPickerFieldRenderer(show_input=False, **jq_options):
    """Color Picker using http://www.syronex.com/software/jquery-color-picker:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.color.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="" id="Sample--color" name="Sample--color" />
        <div id="Sample--color_colors"></div>
        <script type="text/javascript">
          jQuery.fa.colorpicker({name:'Sample--color', options:{"color": ["#FFFFFF", ..., "#FF0096", "#B02B2C", "#000000"]}});
        </script>...
            
    """
    if 'color' not in jq_options:
        jq_options['color'] = [
            "#FFFFFF", "#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70",
            "#006E2E", "#C3D9FF", "#4096EE", "#356AA0", "#FF0096", "#B02B2C",
            "#000000"
            ]
    color = jq_options['color']
    class Renderer(fields.TextFieldRenderer):
        template=templates.get_template('colorpicker.mako')
        def render_readonly(self):
            return '<span style="background-color:%s">&nbsp;</span>' % self._value
        def render(self, **kwargs):
            value=self._value or ''
            try:
                jq_options['defaultColor'] = color.index(value)
            except:
                pass
            kwargs.update(
                name=self.name,
                value=value,
                show_input=show_input,
                jq_options=dumps(jq_options),
            )
            return self.template.render(**kwargs)
    return Renderer

colorpicker = ColorPickerFieldRenderer

class DateFieldRenderer(fields.DateFieldRenderer):
    """Use http://jqueryui.com/demos/datepicker/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.date.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="text" autocomplete="off" size="10" value="" id="Sample--date" name="Sample--date" />
        <script type="text/javascript">
          jQuery(document.getElementById('Sample--date')).datepicker({"dateFormat": "yy-mm-dd"});
        </script>...
        
    """
    template = templates.get_template('date.mako')
    jq_options = dict(dateFormat='yy-mm-dd')
    def render(self, **kwargs):
        value = self._value or ''
        value = value and value.split()[0] or ''
        kwargs.update(
            name=self.name,
            value=value,
            jq_options=dumps(self.jq_options),
        )
        return self.template.render(**kwargs)

    def _serialized_value(self):
        value = self._params.getone(self.name) or ''
        return value

date = DateFieldRenderer

class DateTimeFieldRenderer(DateFieldRenderer, fields.TimeFieldRenderer):
    """Use http://jqueryui.com/demos/datepicker/"""
    format = '%Y-%m-%d %H:%M:%S'
    template = templates.get_template('date.mako')
    jq_options = dict(dateFormat='yy-mm-dd')
    def render(self, **kwargs):
        return h.content_tag('span', DateFieldRenderer.render(self, **kwargs) + ' ' + fields.TimeFieldRenderer._render(self, **kwargs))

    def _serialized_value(self):
        return DateFieldRenderer._serialized_value(self) + ' ' + fields.TimeFieldRenderer._serialized_value(self)

datetime = DateTimeFieldRenderer

class SliderFieldRenderer(fields.IntegerFieldRenderer):
    """Fill an integer field using http://jqueryui.com/demos/slider/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.slider.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="0" id="Sample--slider" name="Sample--slider" />
        <div id="Sample--slider_slider"></div>
        <script type="text/javascript">
          jQuery.fa.slider({name:'Sample--slider'});
        </script>...
    """
    template = templates.get_template('slider.mako')
    def render(self, **kwargs):
        value = self._value or 0
        return self.template.render(name=self.name, value=value)

slider = SliderFieldRenderer

class SelectableFieldRenderer(fields.SelectFieldRenderer):
    """Fill a text field using http://jqueryui.com/demos/selectable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.selectable.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="" id="Sample--selectable" name="Sample--selectable" />
        <div id="Sample--selectable_error" title="Error" style="display:none">
          <p>You can only select one value</p>
        </div>
        <ul id="Sample--selectable_selectable" class="fa_selectable">
        <li class="ui-widget-content" alt="a">a</li>
        <li class="ui-widget-content" alt="b">b</li>
        <li class="ui-widget-content" alt="c">c</li>
        <li class="ui-widget-content" alt="d">d</li>
        <li class="ui-widget-content" alt="e">e</li>
        <li class="ui-widget-content" alt="f">f</li>
        </ul>
        <script type="text/javascript">
          jQuery.fa.selectable({name:'Sample--selectable', sep:';', multiple:false});
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

selectable = SelectableFieldRenderer

default_renderers = {
    types.Date:date,
    types.DateTime:datetime,
    'slider':slider,
    'selectable':selectable,
}
