# -*- coding: utf-8 -*-
from formalchemy.ext.zope import FieldSet
from zope import interface, schema
from renderers import *
from webob import Request, Response

FieldSet.default_renderers.update(default_renderers)

class ISample(interface.Interface):
    title = schema.TextLine(title=u'title')
    selectable = schema.TextLine(title=u'selectable')
    slider = schema.Int(title=u'integer as slider')
    date = schema.Date(title=u'date')
    datetime = schema.Datetime(title=u'datetime')

def application(environ, start_response):
    req = Request(environ)
    resp = Response()
    fs = FieldSet(ISample)
    fs.slider.set(renderer=SliderFieldRenderer)
    fs.selectable.set(renderer=SelectableFieldRenderer, options=[l for l in 'abcdef'])
    obj = fs.gen_model()
    fs = fs.bind(obj, data=req.POST or None)
    template = templates.get_template('index.mako')
    resp.body = template.render(fs=fs)
    return resp(environ, start_response)

def make_app(*args, **kwargs):
    return application
