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

class IAccordion(interface.Interface):
    field1 = schema.TextLine(title=u'field 1')
    field2 = schema.TextLine(title=u'field 2')

fs1 = FieldSet(ITab1)
obj1 = fs1.gen_model()
fs2 = FieldSet(ITab2)
obj2 = fs2.gen_model()
fs3 = FieldSet(IAccordion)
fs3.configure(include=[fs3.field1])
obj3 = fs3.gen_model()
fs4 = FieldSet(IAccordion)
fs4.configure(include=[fs4.field2])

class ISample(interface.Interface):
    title = schema.TextLine(title=u'Autocomplete')
    ajax = schema.TextLine(title=u'Auto complete with an ajax request')
    color = schema.TextLine(title=u'Color picker')
    selectable = schema.TextLine(title=u'Selectable')
    selectable_token = schema.TextLine(title=u'Selectable token - '
                              'Save values as a string separate by a semi comma')
    sortable = schema.TextLine(title=u'Sortable token - '
                              'Save values as a string separate by a semi comma')
    slider = schema.Int(title=u'Integer as slider')
    date = schema.Date(title=u'Date')
    datetime = schema.Datetime(title=u'Datetime')

Form = FieldSet(ISample)
Form.title.set(renderer=AutoCompleteFieldRenderer(['aa', 'bb']))
Form.ajax.set(renderer=AutoCompleteFieldRenderer('/fa.jquery/ajax_values'))
Form.color.set(renderer=ColorPickerFieldRenderer())
Form.slider.set(renderer=SliderFieldRenderer)
Form.selectable.set(renderer=SelectableFieldRenderer, options=[l for l in 'abcdef'])
Form.selectable_token.set(renderer=SelectableTokenFieldRenderer, options=[l for l in 'abcdef'])
Form.sortable.set(renderer=SortableTokenTextFieldRenderer)

obj = Form.gen_model()
obj.context['sortable'] = 'fisrt;second'
fs = Form.bind(obj)

