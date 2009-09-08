# -*- coding: utf-8 -*-
from formalchemy.ext.zope import FieldSet
from zope import interface, schema
from renderers import *

FieldSet.default_renderers.update(default_renderers)

class ITab1(interface.Interface):
    title = schema.TextLine(title=u'title')

class ITab2(interface.Interface):
    title = schema.TextLine(title=u'title')
    description = schema.TextLine(title=u'description')

fs1 = FieldSet(ITab1)
obj1 = fs1.gen_model()
fs2 = FieldSet(ITab2)
obj2 = fs2.gen_model()

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
Form.ajax.set(renderer=AutoCompleteFieldRenderer('/fa.jquery/ajax_values'))
Form.color.set(renderer=ColorPickerFieldRenderer())
Form.slider.set(renderer=SliderFieldRenderer)
Form.selectable.set(renderer=SelectableFieldRenderer, options=[l for l in 'abcdef'])
Form.sortable.set(renderer=SortableTextFieldRenderer)

obj = Form.gen_model()
obj.context['sortable'] = 'fisrt;second'
fs = Form.bind(obj)

