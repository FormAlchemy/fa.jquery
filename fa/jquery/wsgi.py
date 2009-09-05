# -*- coding: utf-8 -*-
from paste.urlparser import StaticURLParser
import glob
import os

jquery_ui = 'jquery-ui-1.7.2.custom'

dirname = os.path.join(os.path.dirname(__file__), jquery_ui)

def html_headers():
    return ''

def StaticApp(*args, **local_conf):
    path = local_conf.get('jquery_ui', dirname)
    return StaticURLParser(path)

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
