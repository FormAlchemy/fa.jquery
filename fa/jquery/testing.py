# -*- coding: utf-8 -*-
from formalchemy.ext.zope import FieldSet
from zope import interface, schema
from renderers import *

FieldSet.default_renderers.update(default_renderers)

class ISample(interface.Interface):
    title = schema.TextLine(title=u'title')
    selectable = schema.TextLine(title=u'selectable')
    slider = schema.Int(title=u'integer as slider')
    date = schema.Date(title=u'date')
    datetime = schema.Datetime(title=u'datetime')

Form = FieldSet(ISample)
Form.slider.set(renderer=SliderFieldRenderer)
Form.selectable.set(renderer=SelectableFieldRenderer, options=[l for l in 'abcdef'])

obj = Form.gen_model()
fs = Form.bind(obj)

