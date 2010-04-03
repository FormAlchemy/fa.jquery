# -*- coding: utf-8 -*-
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
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

