# -*- coding: utf-8 -*-
from webob import Request, Response
from testing import Form

def application(environ, start_response):
    req = Request(environ)
    resp = Response()
    obj = Form.gen_model()
    fs = Form.bind(obj, data=req.POST or None)
    template = templates.get_template('index.mako')
    resp.body = template.render(fs=fs)
    return resp(environ, start_response)


def make_app(*args, **kwargs):
    return application
