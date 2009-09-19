# -*- coding: utf-8 -*-
import os
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
from mako.lookup import TemplateLookup

dirname = os.path.join(os.path.dirname(__file__), 'templates')
templates = TemplateLookup([dirname], input_encoding='utf-8', output_encoding='utf-8')

class TemplateEngine(BaseTemplateEngine):

    def render(self, name, **kwargs):
        template = templates.get_template('/forms/%s.mako' % name)
        return template.render(**kwargs)

