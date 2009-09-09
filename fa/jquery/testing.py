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
    title = schema.TextLine(title=u'Autocomplete')
    ajax = schema.TextLine(title=u'Auto complete with an ajax request')
    color = schema.TextLine(title=u'Color picker')
    selectable = schema.TextLine(title=u'Selectable')
    sortable = schema.TextLine(title=u'Sortable token')
    slider = schema.Int(title=u'Integer as slider')
    date = schema.Date(title=u'Date')
    datetime = schema.Datetime(title=u'Datetime')

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

