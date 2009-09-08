# -*- coding: utf-8 -*-
from webob import Request, Response
from renderers import templates
from forms import Tabs
from testing import *

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
        obj.context['sortable'] = '1;2;3'
        obj.context['selectable'] = 'f'
        fs = Form.bind(obj, data=req.POST or None)

        tabs = Tabs('my_tabs',
                    ('tab1', 'My first tab', fs1),
                    footer='<input type="submit" name="%(id)s" />')
        tabs.append('tab2', 'The second', fs2)
        tabs.tab1 = tabs.tab1.bind(obj1, data=req.POST or None)
        tabs.bind(obj2, 'tab2', data=req.POST or None)
        if req.POST:
            tabs.validate()

        template = templates.get_template('index.mako')
        resp.body = template.render(fs=fs, tabs=tabs)
    return resp(environ, start_response)


def make_app(*args, **kwargs):
    return application
