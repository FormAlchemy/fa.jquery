# -*- coding: utf-8 -*-
from formalchemy.ext.pylons.controller import _ModelsController as Base
from fa.jquery.wsgi import StaticApp

class _ModelsController(Base):
    _static_app=StaticApp()

def ModelsController(cls, prefix_name, member_name, collection_name):
    """wrap a controller with :class:~formalchemy.ext.pylons.controller._ModelsController"""
    return type(cls.__name__, (cls, _ModelsController),
                dict(prefix_name=prefix_name, member_name=member_name, collection_name=collection_name))


