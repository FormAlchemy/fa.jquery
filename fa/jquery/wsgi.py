# -*- coding: utf-8 -*-
from paste.urlparser import StaticURLParser
from webob import Request, Response
from textile import textile
import glob
import os

jquery_ui = 'jquery-ui-1.8rc1.custom'

dirname = os.path.join(os.path.dirname(__file__), jquery_ui)

def html_headers():
    return ''

class Static(StaticURLParser):
    """subclass to add a few helpers like markup preview"""

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path == '/markup_preview.html':
            # markup preview helper
            req = Request(environ)
            resp = Response()
            markup = req.POST.get('markup', 'textile')
            value = req.POST['value']
            try:
                if markup == 'textile':
                    value = textile(value)
                elif markup == 'bbcode':
                    from postmarkup import render_bbcode
                    value = render_bbcode(value)
            except:
                pass
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            resp.body = value
            return resp(environ, start_response)
        return StaticURLParser.__call__(self, environ, start_response)

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
