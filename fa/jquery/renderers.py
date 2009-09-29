# -*- coding: utf-8 -*-
import os
from simplejson import dumps
from formalchemy import helpers as h
from formalchemy import types
from formalchemy import fields
from formalchemy import config

from utils import templates

def jQueryFieldRenderer(plugin, show_input=False, tag='div', renderer=fields.TextFieldRenderer, resources=[], **jq_options):
    """Extending jQuery.fa:

    .. sourcecode:: python

        >>> from testing import fs
        >>> renderer = jQueryFieldRenderer('myplugin', option1=True, option2=['a', 'b'])
        >>> field = fs.title.set(renderer=renderer)
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><input autocomplete="off" id="Sample--title" name="Sample--title" type="text" /></div>
        <div id="Sample--title_myplugin"></div>
        <script type="text/javascript">
          jQuery.fa.myplugin('Sample--title', {"option2": ["a", "b"], "option1": true});
        </script>...

    Then in your javascript code:

    .. sourcecode:: javascript

       jQuery.fa.extend({
            myplugin: function(field, plugin, options) {
                // do what you want
           }
       });

    Where field is the input, plugin the empty div and options the jq_options passed to the renderer.

    """
    template_name = jq_options.get('_template', 'jquery')
    class Renderer(renderer):
        template=templates.get_template('/renderers/%s.mako' % template_name)
        def render(self, **kwargs):
            html = renderer.render(self, autocomplete='off', **kwargs)
            kwargs.update(jq_options)
            options = dict(
                tag=tag,
                html=html,
                plugin=plugin,
                name=self.name,
                show_input=show_input,
                resources=resources,
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

    With more advanced options:

    .. sourcecode:: python

        >>> field = fs.title.set(
        ...     renderer=AutoCompleteFieldRenderer(
        ...         '/my/uri',
        ...         width=320,
        ...         scroll=True,
        ...         scrollHeight=300,
        ...         ))

    """
    jq_options.update(data=url_or_data, show_input=True)
    return jQueryFieldRenderer('autocomplete', renderer=renderer, **jq_options)

autocomplete = AutoCompleteFieldRenderer

def SortableTokenTextFieldRenderer(sep=';', show_input=False, **jq_options):
    """Sortable token using http://jqueryui.com/demos/sortable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.sortable.set(renderer=SortableTokenTextFieldRenderer)
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="fisrt;second" id="Sample--sortable" name="Sample--sortable" />
        <ul id="Sample--sortable_sortable" class="fa_sortable">
        <li class="ui-state-default" alt="fisrt"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>fisrt</li>
        <li class="ui-state-default" alt="second"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>second</li>
        </ul>
        <script type="text/javascript">
          jQuery.fa.sortable('Sample--sortable', {sep:';'});
        </script>...
    """
    class Renderer(fields.TextFieldRenderer):
        template=templates.get_template('/renderers/sortable.mako')
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

sortable_token = SortableTokenTextFieldRenderer

def ColorPickerFieldRenderer(**jq_options):
    """Color Picker using http://www.syronex.com/software/jquery-color-picker:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.color.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><input autocomplete="off" id="Sample--color" name="Sample--color" type="text" /></div>
        <div id="Sample--color_colorpicker"></div>
        <script type="text/javascript">
          jQuery.fa.colorpicker('Sample--color', {"color": ["#FFFFFF", ..., "#FF0096", "#B02B2C", "#000000"]});
        </script>
        <BLANKLINE>
        
        <div style="display:none;"><input autocomplete="off" id="Sample--color" name="Sample--color" type="text" /></div>
        <div id="Sample--color_colors"></div>
        <script type="text/javascript">
          jQuery.fa.colorpicker('Sample--color', {"color": ["#FFFFFF", ..., "#FF0096", "#B02B2C", "#000000"]});
        </script>...

    """
    if 'color' not in jq_options:
        jq_options['color'] = [
            "#FFFFFF", "#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70",
            "#006E2E", "#C3D9FF", "#4096EE", "#356AA0", "#FF0096", "#B02B2C",
            "#000000"
            ]
    return jQueryFieldRenderer('colorpicker', **jq_options)

colorpicker = ColorPickerFieldRenderer

class DateFieldRenderer(fields.DateFieldRenderer):
    """Use http://jqueryui.com/demos/datepicker/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.date.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="text" autocomplete="off" size="10" value="" id="Sample--date" name="Sample--date" />
        <script type="text/javascript">
          jQuery.fa.datepicker('Sample--date', {"dateFormat": "yy-mm-dd"});
        </script>...

    """
    template = templates.get_template('/renderers/date.mako')
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
    template = templates.get_template('/renderers/date.mako')
    jq_options = dict(dateFormat='yy-mm-dd')
    def render(self, **kwargs):
        return h.content_tag('span', DateFieldRenderer.render(self, **kwargs) + ' ' + fields.TimeFieldRenderer._render(self, **kwargs))

    def _serialized_value(self):
        date = DateFieldRenderer._serialized_value(self)
        if date:
            return date + ' ' + fields.TimeFieldRenderer._serialized_value(self)
        else:
            return ''

datetime = DateTimeFieldRenderer

def SliderFieldRenderer(min=0, max=100, show_value=True, **jq_options):
    """Fill an integer field using http://jqueryui.com/demos/slider/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.slider.set(renderer=SliderFieldRenderer(min=10, max=150))
    """
    jq_options.update(min=min, max=max, show_value=show_value)
    return jQueryFieldRenderer('slider', renderer=fields.IntegerFieldRenderer, **jq_options)

slider = SliderFieldRenderer

class SelectableFieldRenderer(fields.SelectFieldRenderer):
    """Fill a text field using http://jqueryui.com/demos/selectable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.selectable.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="" id="Sample--selectable" name="Sample--selectable" />
        <ul id="Sample--selectable_selectable" class="fa_selectable">
        <li class="ui-widget-content" alt="a">a</li>
        <li class="ui-widget-content" alt="b">b</li>
        <li class="ui-widget-content" alt="c">c</li>
        <li class="ui-widget-content" alt="d">d</li>
        <li class="ui-widget-content" alt="e">e</li>
        <li class="ui-widget-content" alt="f">f</li>
        </ul>
        <script type="text/javascript">
          jQuery.fa.selectable('Sample--selectable', {"multiple": false});
        </script>...

    """
    multiple=False
    sep=';'
    template = templates.get_template('/renderers/selectable.mako')
    def render(self, options, **kwargs):
        name = self.name
        value = self._value or ''
        if callable(options):
            L = fields._normalized_options(options(self.field.parent))
        else:
            L = list(options)
        if len(L) > 0:
            if len(L[0]) == 2:
                L = [(k, self.stringify_value(v)) for k, v in L]
            else:
                L = [fields._stringify(k) for k in L]
                L = [(k, k) for k in L]
        jq_options=dict(multiple=self.multiple)
        if self.multiple:
            jq_options['sep'] = self.sep
        return self.template.render(name=name, value=value, options=L, jq_options=dumps(jq_options))

selectable = SelectableFieldRenderer

class SelectableTokenFieldRenderer(SelectableFieldRenderer):
    """Same as SelectFieldRenderer but allow multiple selection saved as
    token:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.selectable.set(renderer=SelectableTokenFieldRenderer)
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <input type="hidden" value="" id="Sample--selectable" name="Sample--selectable" />
        ...
        <script type="text/javascript">
          jQuery.fa.selectable('Sample--selectable', {"multiple": true, "sep": ";"});
        </script>...
    """
    multiple = True

default_renderers = {
    types.Date:date,
    types.DateTime:datetime,
    'slider':slider,
    'selectable':selectable,
}
