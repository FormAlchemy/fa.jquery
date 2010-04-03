# -*- coding: utf-8 -*-
import os
from simplejson import dumps
from webhelpers.html import literal
from formalchemy import helpers as h
from formalchemy import types
from formalchemy import fields
from formalchemy import config
from postmarkup import render_bbcode
from textile import textile as render_textile

from utils import templates
from utils import url

__doc__ = """
This is the predefined renderers. You can have a look at the :doc:`../demo`.

If you need your own, use the :class:`~fa.jquery.renderers.jQueryFieldRenderer`
as base class.

Some plugins use extra resources stored at the
:class:`~fa.jquery.wsgi.StaticApp`. By default the prefix used is ``/jquery``.
If you want to change this you can use this snippet:

.. sourcecode: python

    >>> from fa.jquery import renderers
    >>> renderers.url.root_url = '/jquery'

"""

def alias(obj, **alias_kwargs):
    """decorator to make aliases with docs"""
    def wrapped(func):
        if hasattr(obj, 'func_name'):
            def wrapper(*args, **kwargs):
                """Alias for :func:`~fa.jquery.renderers.%s` with preset options %r""" % (obj.func_name, alias_kwargs)
                kwargs.update(alias_kwargs)
                return obj(*args, **kwargs)
            wrapper.func_name = func.func_name
            wrapper.func_doc = """Alias for :func:`~fa.jquery.renderers.%s` with preset options %r""" % (obj.func_name, alias_kwargs)
            return wrapper
        else:
            doc = """Alias for :class:`~fa.jquery.renderers.%s` with preset options %r""" % (obj.__name__, alias_kwargs)
            alias_kwargs['__doc__'] = doc
            return type(func.func_name, (obj,), alias_kwargs)
    return wrapped

def jQueryFieldRenderer(plugin, show_input=False, tag='div', renderer=fields.TextFieldRenderer,
                        resources_prefix=None, resources=[], **jq_options):
    """Extending jQuery.fa:

    .. sourcecode:: python

        >>> from testing import fs
        >>> renderer = jQueryFieldRenderer('myplugin', option1=True, option2=['a', 'b'])
        >>> field = fs.title.set(renderer=renderer)
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><input autocomplete="off" id="Sample--title" name="Sample--title" type="text" /></div>
        <div id="Sample--title_myplugin"></div>
        <script type="text/javascript">
          jQuery.fa.myplugin('Sample--title', {"option2": ["a", "b"], "options": [], "option1": true});
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
    template=templates.get_template('/renderers/%s.mako' % template_name)
    class Renderer(renderer):
        def render(self, **kwargs):
            html = renderer.render(self, autocomplete='off', **kwargs)
            kwargs.update(self.jq_options)
            options = dict(
                tag=tag,
                html=html,
                plugin=plugin,
                name=self.name,
                show_input=show_input,
                resources=[url(r, prefix=self.resources_prefix) for r in resources],
            )
            try:
                options.update(options=dumps(kwargs))
            except TypeError:
                options.update(options={})
            try:
                return literal(self.template.render(**options))
            except:
                raise ValueError('Invalid options: %s' % options)
    return type('%sPluginRenderer' % plugin.title(), (Renderer,),
                dict(template=template,
                     jq_options=jq_options,
                     resources_prefix=resources_prefix))

@alias(jQueryFieldRenderer)
def plugin(): pass

def AutoCompleteFieldRenderer(url_or_data, renderer=fields.TextFieldRenderer, **jq_options):
    """Use http://docs.jquery.com/UI/Autocomplete:

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
    jq_options.update(source=url_or_data, show_input=True)
    return jQueryFieldRenderer('autocomplete', renderer=renderer, **jq_options)

@alias(AutoCompleteFieldRenderer)
def autocomplete(): pass

def SortableTokenTextFieldRenderer(sep=';', show_input=False, **jq_options):
    """Sortable token using http://jqueryui.com/demos/sortable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.sortable.set(renderer=SortableTokenTextFieldRenderer())
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
            return literal(self.template.render(**kwargs))
    return Renderer

@alias(SortableTokenTextFieldRenderer)
def sortable_token(): pass

def ColorPickerFieldRenderer(colors=[], **jq_options):
    """Color Picker using http://www.syronex.com/software/jquery-color-picker:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.color.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><input autocomplete="off" id="Sample--color" name="Sample--color" type="text" /></div>
        <div id="Sample--color_colorpicker"></div>
        <script type="text/javascript">
          jQuery.fa.colorpicker('Sample--color', {"color": ["#FFFFFF", ...]});
        </script>
        <BLANKLINE>
        
        <div style="display:none;"><input autocomplete="off" id="Sample--color" name="Sample--color" type="text" /></div>
        <div id="Sample--color_colors"></div>
        <script type="text/javascript">
          jQuery.fa.colorpicker('Sample--color', {"color": ["#FFFFFF", ..., "#FF0096", "#B02B2C", "#000000"]});
        </script>...

    """
    jq_options['color'] = colors or [
            "#FFFFFF", "#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70",
            "#006E2E", "#C3D9FF", "#4096EE", "#356AA0", "#FF0096", "#B02B2C",
            "#000000"
            ]
    return jQueryFieldRenderer('colorpicker', **jq_options)

@alias(ColorPickerFieldRenderer)
def colorpicker(): pass

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
        return literal(self.template.render(**kwargs))

    def _serialized_value(self):
        value = self.params.getone(self.name) or ''
        return value

@alias(DateFieldRenderer)
def date(): pass

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

@alias(DateTimeFieldRenderer)
def datetime(): pass

def SliderFieldRenderer(min=0, max=100, show_value=True, **jq_options):
    """Fill an integer field using http://jqueryui.com/demos/slider/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> field = fs.slider.set(renderer=SliderFieldRenderer(min=10, max=150))
    """
    jq_options.update(min=min, max=max, show_value=show_value)
    return jQueryFieldRenderer('slider', renderer=fields.IntegerFieldRenderer, **jq_options)

@alias(SliderFieldRenderer)
def slider(): pass

def SelectableFieldRenderer(multiple=False, **jq_options):
    """Fill a text field using http://jqueryui.com/demos/selectable/:

    .. sourcecode:: python

        >>> from testing import fs
        >>> print fs.selectable.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div style="display:none;"><select autocomplete="off" id="Sample--selectable" name="Sample--selectable">
        <option value="a">a</option>
        <option value="b">b</option>
        <option value="c">c</option>
        <option value="d">d</option>
        <option value="e">e</option>
        <option value="f">f</option>
        </select></div>
        <div id="Sample--selectable_selectable"></div>
        <script type="text/javascript">
          jQuery.fa.selectable('Sample--selectable', {"multiple": false, "options": ["a", "b", "c", "d", "e", "f"]});
        </script>

    """
    jq_options.update(multiple=multiple)
    class Renderer(fields.SelectFieldRenderer):
        def render(self, *args, **kwargs):
            kwargs['multiple'] = self.multiple
            return fields.SelectFieldRenderer.render(self, *args, **kwargs)
    return jQueryFieldRenderer('selectable',
                               renderer=type('SelectableFieldRenderer', (Renderer,), dict(multiple=multiple)),
                               **jq_options)

@alias(SelectableFieldRenderer, multiple=False)
def selectable():pass

@alias(SelectableFieldRenderer, multiple=True)
def selectables():pass

def RichTextFieldRenderer(use='tinymce', resources_prefix=None, **jq_options):
    """RichTextFieldRenderer using TinyMCE or MarkitUp!:

    .. sourcecode: python

        >>> from testing import fs
        >>> field = fs.rich.set(renderer=RichTextFieldRenderer(use='tinymce', theme='advanced'))
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/jquery/tiny_mce/tiny_mce.js");
          jQuery.fa.add_resource("/jquery/tiny_mce/jquery.tinymce.js");
        </script>
        <textarea autocomplete="off" id="Sample--rich" name="Sample--rich"></textarea>
        <div id="Sample--rich_tinymce"></div>
        <script type="text/javascript">
          jQuery.fa.tinymce('Sample--rich', {... "theme": "advanced", ...});
        </script>

    If you want to use your own TinyMCE/MarkitUp! version:

    .. sourcecode: python

        >>> field = fs.rich.set(renderer=RichTextFieldRenderer(use='tinymce', resources_prefix='/my_js'))
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/my_js/tiny_mce/tiny_mce.js");
          jQuery.fa.add_resource("/my_js/tiny_mce/jquery.tinymce.js");
        </script>
        ...

    There is also some aliases:

    .. sourcecode: python

        >>> field = fs.rich.set(renderer=tinymce())
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/jquery/tiny_mce/tiny_mce.js");
          jQuery.fa.add_resource("/jquery/tiny_mce/jquery.tinymce.js");
        </script>
        <textarea autocomplete="off" id="Sample--rich" name="Sample--rich"></textarea>
        <div id="Sample--rich_tinymce"></div>
        <script type="text/javascript">
          jQuery.fa.tinymce('Sample--rich', {... "theme": "advanced", ...});
        </script>

        >>> field = fs.rich.set(renderer=textile())
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/jquery/markitup/jquery.markitup.pack.js");
          jQuery.fa.add_resource("/jquery/markitup/skins/simple/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/textile/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/textile/set.js");
        </script>
        <textarea autocomplete="off" id="Sample--rich" name="Sample--rich"></textarea>
        <div id="Sample--rich_markitup"></div>
        <script type="text/javascript">
          jQuery.fa.markitup('Sample--rich', {... "nameSpace": "textile", ...});
        </script>
        
        >>> field = fs.rich.set(renderer=markdown())
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/jquery/markitup/jquery.markitup.pack.js");
          jQuery.fa.add_resource("/jquery/markitup/skins/simple/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/markdown/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/markdown/set.js");
        </script>
        <textarea autocomplete="off" id="Sample--rich" name="Sample--rich"></textarea>
        <div id="Sample--rich_markitup"></div>
        <script type="text/javascript">
          jQuery.fa.markitup('Sample--rich', {... "nameSpace": "markdown", ...});
        </script>

        >>> field = fs.rich.set(renderer=bbcode())
        >>> print field.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <script type="text/javascript">
          jQuery.fa.add_resource("/jquery/markitup/jquery.markitup.pack.js");
          jQuery.fa.add_resource("/jquery/markitup/skins/simple/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/bbcode/style.css");
          jQuery.fa.add_resource("/jquery/markitup/sets/bbcode/set.js");
        </script>
        <textarea autocomplete="off" id="Sample--rich" name="Sample--rich"></textarea>
        <div id="Sample--rich_markitup"></div>
        <script type="text/javascript">
          jQuery.fa.markitup('Sample--rich', {... "nameSpace": "bbcode", ...});
        </script>

    """
    plugin_name = use
    defaults = {}
    if use == 'tinymce':
        resources = ['tiny_mce/tiny_mce.js', 'tiny_mce/jquery.tinymce.js']
        defaults['theme'] = 'advanced'
        defaults['theme_advanced_toolbar_location'] = "top"
        defaults['theme_advanced_toolbar_align'] = "left"
        defaults['theme_advanced_statusbar_location'] = "bottom"
        defaults['theme_advanced_resizing'] = True
        if 'content_css' in jq_options:
            jq_options['content_css'] = [url(c, prefix=resources_prefix) for c in jq_options['content_css']]
    elif use in ('textile', 'bbcode', 'markdown'):
        plugin_name = 'markitup'
        defaults['nameSpace'] = use
        defaults['resizeHandle'] = True
        defaults['previewAutoRefresh'] = True
        defaults['previewParserPath'] = url('markup_parser.html?markup=%s' % use)
        resources = ['markitup/jquery.markitup.pack.js',
                     'markitup/skins/simple/style.css',
                     'markitup/sets/%s/style.css' % use,
                     'markitup/sets/%s/set.js' % use]

    else:
        resources = []

    for k, v in defaults.items():
        if k not in jq_options:
            jq_options[k] = v

    class Renderer(fields.TextAreaFieldRenderer):
        markup = use

        def render_textile(self, **kwargs):
            value = self._value
            return value and render_textile(value) or ''

        def render_bbcode(self, **kwargs):
            value = self._value
            return value and render_bbcode(value) or ''

        def render_readonly(self, **kwargs):
            meth = getattr(self, 'render_%s' % self.markup, None)
            if meth is not None:
                return meth()
            return fields.TextAreaFieldRenderer.render(self, **kwargs)
    return jQueryFieldRenderer(plugin_name, show_input=True, renderer=Renderer,
                               resources_prefix=resources_prefix, resources=resources, **jq_options)

@alias(RichTextFieldRenderer, use='tinymce')
def tinymce(): pass

@alias(RichTextFieldRenderer, use='textile')
def textile(): pass

@alias(RichTextFieldRenderer, use='markdown')
def markdown(): pass

@alias(RichTextFieldRenderer, use='bbcode')
def bbcode(): pass

default_renderers = {
    types.Date:date,
    types.DateTime:datetime,
    types.HTML: tinymce(),
    types.Slider: slider,
    types.Color: ColorPickerFieldRenderer,
    types.Selectable: selectable(),
    types.Selectables: selectables(),
}

