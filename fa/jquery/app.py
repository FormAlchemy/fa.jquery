# -*- coding: utf-8 -*-
from webob import Request, Response
from renderers import templates
from forms import Tabs
from testing import *

class Demo(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.path.endswith('/fa.jquery/ajax_values'):
            resp = Response()
            resp.body = '\n'.join(['Ajax','Borax','Corax', 'Dorax','Manix'])
        elif req.path.endswith('/fa.jquery/demo.html'):
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
            body = template.render(fs=fs, tabs=tabs, headers=req.GET.get('headers', False))

            req.method = 'get'
            resp = req.get_response(self.app)
            resp.body = resp.body.replace('<div id="demo"/>', body)
        else:
            return self.app(environ, start_response)
        return resp(environ, start_response)


def make_app(global_config, **kwargs):
    import os
    from paste.urlparser import StaticURLParser
    app = StaticURLParser(os.path.join(global_config['here'], 'docs/_build/html'))
    return Demo(app)

def make_demo(*args, **kwargs):
    def filter(app):
        return Demo(app)
    return filter

