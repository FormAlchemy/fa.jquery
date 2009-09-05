# -*- coding: utf-8 -*-
from formalchemy.ext.zope import FieldSet
from zope import interface, schema
from renderers import templates, default_renderers
from webob import Request, Response

FieldSet.default_renderers.update(default_renderers)

class ISample(interface.Interface):
    title = schema.TextLine(title=u'title')
    date = schema.Date(title=u'date')

def application(environ, start_response):
    req = Request(environ)
    resp = Response()
    fs = FieldSet(ISample)
    obj = fs.gen_model()
    fs = fs.bind(obj)
    template = templates.get_template('index.mako')
    resp.body = template.render(fs=fs)
    return resp(environ, start_response)

def make_app(*args, **kwargs):
    return application
