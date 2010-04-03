# -*- coding: utf-8 -*-
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
from formalchemy import types as fatypes
from webhelpers.html import escape, literal
from mako.lookup import TemplateLookup
from simplejson import dumps
import logging
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

    .. sourcecode: python

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

    .. sourcecode: python

        >>> f = Flash()
        >>> f.info('my info')
        >>> f.warn('my warn')
        >>> print f.render() #doctest: +NORMALIZE_WHITESPACE
        jQuery(document).ready(function{
        jQuery.jGrowl("my info", {"theme": "info"});
        jQuery.jGrowl("my warn", {"theme": "warn"});
        });

    """
    cssClasses = {
            logging.INFO: 'info',
            logging.WARN: 'warn',
            logging.ERROR: 'error',
            logging.DEBUG: 'debug',
        }
    def __init__(self, level=logging.INFO):
        self.messages = []
        self.level = level

    def log(self, message, level=logging.INFO):
        if level >= self.level:
            self.messages.append((message, level))

    def info(self, message):
        """info level"""
        self.log(message)

    def warn(self, message):
        """warn level"""
        self.log(message, logging.WARN)

    def error(self, message):
        """error level"""
        self.log(message, logging.ERROR)

    def debug(self, message):
        """debug level"""
        self.log(message, logging.DEBUG)

    def render(self, onload=True):
        template=templates.get_template('/utils/flash.mako')
        messages = []
        for message, level in self.messages:
            message = dumps([message, dict(theme=self.cssClasses[level])])
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
