# -*- coding: utf-8 -*-
from paste.urlparser import StaticURLParser
import os

jquery_ui = 'jquery-ui-1.7.2.custom'

dirname = os.path.join(os.path.dirname(__file__), jquery_ui)

def html_headers():
    return ''

def StaticApp(*args, **local_conf):
    path = local_conf.get('jquery_ui', dirname)
    return StaticURLParser(path)

