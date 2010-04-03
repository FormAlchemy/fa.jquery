# -*- coding: utf-8 -*-
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
from formalchemy import types as fatypes
from webhelpers.html import escape, literal
from mako.lookup import TemplateLookup
from simplejson import dumps
import logging
import random
import os

dirname = os.path.join(os.path.dirname(__file__), 'templates')
templates = TemplateLookup([dirname], input_encoding='utf-8', output_encoding='utf-8')

class TemplateEngine(BaseTemplateEngine):

    def __init__(self, *dirnames, **kwargs):
        options = dict(input_encoding='utf-8', output_encoding='utf-8')
        options.update(kwargs)
        dirnames = list(dirnames)
        try:
            from pylons import config
        except ImportError:
            pass
        else:
            dirnames[0:0] = config['pylons.paths']['templates']
        dirnames.append(dirname)
        self.templates = TemplateLookup(dirnames, **options)

    def render(self, name, **kwargs):
        name = name.strip('/')
        if not name.endswith('.mako'):
            name = '%s.mako' % name
        template = self.templates.get_template('/forms/%s' % name)
        return literal(template.render(**kwargs))

def url(*args, **kwargs):
    """return a path to script. you can change the root_url. default to `/jquery`:

    .. sourcecode:: python

        >>> url.root_url = '/path_to_static'
        >>> print url('/absolute.js')
        /absolute.js
        >>> print url('relative', 'plugin.js')
        /path_to_static/relative/plugin.js
        >>> print url('..', 'plugin.js')
        /path_to_static/../plugin.js
        >>> print url('plugin.js', prefix='/my_js')
        /my_js/plugin.js
    """
    if args and not args[0].startswith('/'):
        args = list(args)
        if kwargs.get('prefix'):
            args.insert(0, kwargs['prefix'])
        else:
            args.insert(0, url.root_url)
    return '/'.join([args[0].rstrip('/')]+[a.strip('/') for a in args[1:]])
url.root_url = '/jquery'

class Flash(object):
    """Flash messaging using jQGrowl:

    .. sourcecode:: python

        >>> f = Flash()
        >>> f.info('my info')
        >>> f.warn('my warn')
        >>> print f.render() #doctest: +NORMALIZE_WHITESPACE
        <script language="javascript">
        jQuery(document).ready(function () {
        jQuery.jGrowl("my info", {"header": "Info", "theme": "ui-state-info", "life": 2000});
        jQuery.jGrowl("my warn", {"header": "Warning", "theme": "ui-state-warning", "life": 3000});
        });
        </script>

    You can also render messages inline:

    .. sourcecode:: python

        >>> print f.render_inline() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div class="jGrowl" style="position:relative;">
        <div id="message_..." style="width:auto;display:none;" class="jGrowl-notification ui-state-highlight ui-corner-all ui-state-info">
        <div class="header">Info</div>
        my info
        </div>
        <div id="message_..." style="width:auto;display:none;" class="jGrowl-notification ui-state-highlight ui-corner-all ui-state-warning">
        <div class="header">Warning</div>
        my warn
        </div>
        <script language="javascript">
        jQuery(document).ready(function () {
        jQuery("#message_...").slideDown('slow', function() {
        var self = $(this);setTimeout(function() { self.slideUp('slow', function(){self.remove();}); }, 20...);
        });
        jQuery("#message_...").slideDown('slow', function() {
        var self = $(this);setTimeout(function() { self.slideUp('slow', function(){self.remove();}); }, 30...);
        });
        });
        </script>
        </div>


    """
    def __init__(self, level=logging.INFO, show_headers=True, options={}):
        self.messages = []
        self.level = level
        self.show_headers = show_headers
        self.options = {
                logging.INFO: {'header': 'Info', 'theme': 'ui-state-info'},
                logging.WARN: {'header': 'Warning', 'theme': 'ui-state-warning'},
                logging.ERROR: {'header': 'Error', 'theme': 'ui-state-error'},
                logging.CRITICAL: {'header': 'Critical', 'theme': 'ui-state-error', 'sticky': True},
                logging.DEBUG: {'header': 'Debug', 'theme': 'ui-state-debug'},
            }
        self.options.update(options)

    def log(self, message, level=logging.INFO):
        if level >= self.level:
            self.messages.append((message, level))

    def info(self, message):
        """info level"""
        self.log(message)

    def warn(self, message):
        """warn level"""
        self.log(message, logging.WARN)
    warning = warn

    def err(self, message):
        """error level"""
        self.log(message, logging.ERROR)
    error = err

    def critical(self, message):
        """critical level"""
        self.log(message, logging.CRITICAL)

    def debug(self, message):
        """debug level"""
        self.log(message, logging.DEBUG)

    def render_inline(self):
        """render the notifications inplace
        """
        template=templates.get_template('/utils/inline_flash.mako')
        messages = []
        lifes = []
        for message, level in self.messages:
            options = self.options[level].copy()
            if not self.show_headers and 'header' in option:
                options.pop('header')
            id = 'message_%s' % str(random.random())[2:]
            messages.append((id, options['theme'], options.get('header'), message))
            if 'life' not in options and 'sticky' not in options:
                if level < 20:
                    level = 20
                lifes.append((id, level*100+random.randint(10, 100)))
            else:
                lifes.append((id, 0))
        return literal(template.render(messages=messages, lifes=lifes, show_headers=self.show_headers))

    def render(self, onload=True):
        """render notification using jGrowl"""
        template=templates.get_template('/utils/flash.mako')
        messages = []
        for message, level in self.messages:
            options = self.options[level].copy()
            if not self.show_headers and 'header' in option:
                options.pop('header')
            if 'life' not in options:
                if level < 20:
                    level = 20
                options['life'] = level*100
            message = dumps([message, options])
            messages.append(message.strip('[]'))
        return literal(template.render(messages=messages, onload=onload))

class Color(fatypes.String):
    """Alias of fatypes.String to bind a ColorPickerFieldRenderer"""
fatypes.Color = Color

class HTML(fatypes.Text):
    """Alias of fatypes.Text to bind a RichTextFieldRenderer"""
fatypes.HTML = HTML

class Slider(fatypes.Integer):
    """Alias of fatypes.Integer to bind a SliderFieldRenderer"""
fatypes.Slider = Slider

class Selectable(fatypes.String):
    """Alias of fatypes.String to bind a selectable()"""
fatypes.Selectable = Selectable

class Selectables(fatypes.List):
    """Alias of fatypes.List to bind a selectables()"""
fatypes.Selectables = Selectables
