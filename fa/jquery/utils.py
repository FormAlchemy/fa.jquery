# -*- coding: utf-8 -*-
import os
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
from webhelpers.html import escape, literal
from mako.lookup import TemplateLookup

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

