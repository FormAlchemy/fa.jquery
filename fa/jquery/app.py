# -*- coding: utf-8 -*-
from webob import Request, Response
from renderers import templates
from testing import Form

def application(environ, start_response):
    req = Request(environ)
    resp = Response()

    if req.path_info.startswith('/values'):
        resp.body = '''Ajax
Borax
Corax
Dorax
Manix
'''
    else:
        obj = Form.gen_model()
        fs = Form.bind(obj, data=req.POST or None)
        template = templates.get_template('index.mako')
        resp.body = template.render(fs=fs)
    return resp(environ, start_response)


def make_app(*args, **kwargs):
    return application
