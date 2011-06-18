# -*- coding: utf-8 -*-
from webob import Request, Response
from renderers import templates
from formalchemy import config
from utils import TemplateEngine, Flash
from forms import Tabs, Accordion
import simplejson
from testing import *

engine = config.engine = TemplateEngine()

class Demo(object):

    def __init__(self, app, headers=False):
        self.app = app
        self.headers = headers

    def __call__(self, environ, start_response):
        req = Request(environ)
        req.flash = Flash()
        req.flash.info('info message display with Flash.render()')
        req.flash.warn('warning message')
        req.flash.error('error message')
        req.flash.critical('critical message is sticky')
        req.inline_flash = Flash()
        req.inline_flash.info('info message display with Flash.render_inline()')
        req.inline_flash.warn('warning message')
        req.inline_flash.error('error message')
        req.inline_flash.critical('critical message is sticky')
        if req.path.endswith('/fa.jquery/ajax_values'):
            resp = Response()
            resp.content_type='application/json'
            resp.body = simplejson.dumps([{'value':'Ajax'},{'value':'Borax'},{'value':'Corax'}, {'value':'Dorax'},{'value':'Manix'}])
        elif req.path.endswith('/fa.jquery/demo.html'):
            req.remove_conditional_headers()
            script_name = req.environ.get('HTTP_X_FORWARDED_PATH', '')
            Form.ajax.set(renderer=AutoCompleteFieldRenderer(script_name+'/fa.jquery/ajax_values'))
            obj = Form.gen_model()
            obj.context['slider'] = '10'
            obj.context['sortable'] = '1;2;3'
            obj.context['radioset'] = 'd'
            obj.context['checkboxset'] = ['b', 'a']
            obj.context['selectable'] = 'f'
            obj.context['selectables'] = ['b', 'c']
            fs = Form.bind(obj, data=req.POST or None)
            fs.engine = engine

            fs1.engine = engine
            fs2.engine = engine
            fs3.engine = engine
            fs4.engine = engine

            tabs = Tabs('my_tabs',
                        ('tab1', 'My first tab', fs1),
                        ('tab2', 'The second', fs2),
                        footer='<input type="submit" name="%(id)s" />')
            tabs.tab1.rebind(fs1.gen_model(), data=req.POST or None)
            tabs.tab2.rebind(fs2.gen_model(), data=req.POST or None)
            accordion = Accordion('my_accordion',
                        ('tab1', 'My first section', fs3),
                        ('tab2', 'The second', fs4),
                        footer='<input type="submit" name="%(id)s" />')
            accordion.tab1.rebind(fs3.gen_model(), data=req.POST or None)
            accordion.tab2.rebind(fs4.gen_model(), data=req.POST or None)
            if req.POST:
                if fs.validate():
                    fs.sync()
                if tabs.validate():
                    tabs.sync()
                if accordion.validate():
                    accordion.sync()

            template = templates.get_template('index.mako')
            head = templates.get_template('head.mako').render()
            body = template.render(req=req, fs=fs, tabs=tabs, accordion=accordion,
                                   headers=self.headers,
                                   head=head, mim=req.GET.get('mim', False))

            if self.headers:
                resp = Response()
                resp.body = body
            else:
                req.method = 'get'
                resp = req.get_response(self.app)
                resp.body = resp.body.replace('</head>', head+'</head>')
                resp.body = resp.body.replace('<div id="demo"></div>', body)
        else:
            return self.app(environ, start_response)
        return resp(environ, start_response)


def make_app(global_config, **kwargs):
    import os
    from paste.urlparser import StaticURLParser
    app = StaticURLParser(os.path.join(global_config['here'], 'docs/_build/html'))
    return Demo(app, headers=True)

def make_demo(*args, **kwargs):
    def filter(app):
        return Demo(app)
    return filter

