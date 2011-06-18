# -*- coding: utf-8 -*-
from webob import Request
from fa.jquery import utils

class PyramidRequest(Request):

    def static_url(self, *args, **kwargs):
        return 'http://localhost/resource.js'

def test_static():
    """
    >>> request = Request.blank('/')
    >>> utils.url('package:static/resource.js', request=request)
    '/path_to_static/package:static/resource.js'

    >>> request = PyramidRequest.blank('/')
    >>> utils.url('package:static/resource.js', request=request)
    'http://localhost/resource.js'
    """


