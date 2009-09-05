# -*- coding: utf-8 -*-
import os
from formalchemy import helpers as h
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
        value = self._value or ''
        value = value and value.split()[0] or ''
        kwargs.update(
            name=self.name,
            value=value,
            jq_options=self.jq_options,
        )
        return self.template.render(**kwargs)

    def _serialized_value(self):
        value = self._params.getone(self.name) or ''
        return value

class DateTimeFieldRenderer(DateFieldRenderer, fields.TimeFieldRenderer):
    format = '%Y-%m-%d %H:%M:%S'
    template = templates.get_template('date.mako')
    jq_options = "{dateFormat:'yy-mm-dd'}"
    def render(self, **kwargs):
        return h.content_tag('span', DateFieldRenderer.render(self, **kwargs) + ' ' + fields.TimeFieldRenderer._render(self, **kwargs))

    def _serialized_value(self):
        return DateFieldRenderer._serialized_value(self) + ' ' + fields.TimeFieldRenderer._serialized_value(self)

class SliderFieldRenderer(fields.IntegerFieldRenderer):
    template = templates.get_template('slider.mako')
    def render(self, **kwargs):
        value = self._value or 0
        return self.template.render(name=self.name, value=value)

class SelectableFieldRenderer(fields.SelectFieldRenderer):
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


default_renderers = {
    types.Date:DateFieldRenderer,
    types.DateTime:DateTimeFieldRenderer,
}
