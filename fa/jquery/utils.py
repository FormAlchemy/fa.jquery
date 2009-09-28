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
        dirnames.append(dirname)
        self.templates = TemplateLookup(dirnames, **options)

    def render(self, name, **kwargs):
        template = self.templates.get_template('/forms/%s.mako' % name)
        return literal(template.render(**kwargs))

