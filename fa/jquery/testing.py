# -*- coding: utf-8 -*-
from formalchemy.ext.zope import FieldSet
from zope import interface, schema
from renderers import *

FieldSet.default_renderers.update(default_renderers)

class ISample(interface.Interface):
    title = schema.TextLine(title=u'title')
    ajax = schema.TextLine(title=u'ajax')
    color = schema.TextLine(title=u'color')
    selectable = schema.TextLine(title=u'selectable')
    sortable = schema.TextLine(title=u'sortable')
    slider = schema.Int(title=u'integer as slider')
    date = schema.Date(title=u'date')
    datetime = schema.Datetime(title=u'datetime')

Form = FieldSet(ISample)
Form.title.set(renderer=AutoCompleteFieldRenderer(['aa', 'bb']))
Form.ajax.set(renderer=AutoCompleteFieldRenderer('/values'))
Form.color.set(renderer=ColorPickerFieldRenderer())
Form.slider.set(renderer=SliderFieldRenderer)
Form.selectable.set(renderer=SelectableFieldRenderer, options=[l for l in 'abcdef'])
Form.sortable.set(renderer=SortableTextFieldRenderer)

obj = Form.gen_model()
obj.context['sortable'] = 'fisrt;second'
fs = Form.bind(obj)

