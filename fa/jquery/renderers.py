# -*- coding: utf-8 -*-
import os
from formalchemy import types
from formalchemy import fields
from formalchemy import config
from mako.lookup import TemplateLookup

dirname = os.path.join(os.path.dirname(__file__), 'templates')
templates = TemplateLookup([dirname], input_encoding='utf-8', output_encoding='utf-8')

class TextFieldRenderer(fields.TextFieldRenderer):
    pass

class DateFieldRenderer(fields.DateFieldRenderer):
    template = templates.get_template('date.mako')
    jq_options = "{dateFormat:'yy-mm-dd'}"
    def render(self, **kwargs):
        return self.template.render(name=self.name,
                                    jq_options=self.jq_options,
                                    **kwargs)

class DateTimeFieldRenderer(fields.DateTimeFieldRenderer):
    pass


default_renderers = {
    types.Date:DateFieldRenderer,
}
