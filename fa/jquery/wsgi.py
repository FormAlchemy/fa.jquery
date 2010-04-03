# -*- coding: utf-8 -*-
from paste.urlparser import StaticURLParser
from webob import Request, Response
from textile import textile
from postmarkup import render_bbcode
import markdown
import glob
import os

jquery_ui = 'jquery-ui'

dirname = os.path.join(os.path.dirname(__file__), jquery_ui)

def html_headers():
    return ''

class Static(StaticURLParser):
    """subclass to add a few helpers like markup preview"""

    def static_app(self, environ, start_response):
        return StaticURLParser.__call__(self, environ, start_response)

    def __call__(self, environ, start_response):
        req = Request(environ)
        if '/markup_parser.html' in req.path_info:
            resp = Response()
            # markup preview helper
            resp.charset = 'utf-8'
            markup = req.GET.get('markup', 'textile')
            value = req.POST.get('data')
            if markup == 'textile':
                value = textile(value)
            elif markup == 'markdown':
                value = markdown.markdown(value)
            elif markup == 'bbcode':
                value = render_bbcode(value)
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            resp.body = value
        else:
            resp = req.get_response(self.static_app)
        resp.headers['X-Salade'] = 'none'
        return resp(environ, start_response)

def StaticApp(*args, **local_conf):
    path = local_conf.get('jquery_ui', dirname)
    return Static(path)

doc = """paste entry point. Generate a StaticURLParser to serve js stuff.

Available files:

"""
for name in os.listdir(dirname):
    filenames = []
    for ext in ('css', 'js'):
        for filename in glob.glob(os.path.join(dirname, name, '*.%s' % ext)):
            if os.path.isfile(filename):
                filenames.append(filename)
        for filename in glob.glob(os.path.join(dirname, name, '*', '*.%s' % ext)):
            if os.path.isfile(filename):
                filenames.append(filename)
    for filename in sorted(filenames):
        doc += '- `%s`\n' % filename.replace(dirname, '')

StaticApp.__doc__ = doc
del doc
