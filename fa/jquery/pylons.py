# -*- coding: utf-8 -*-
from formalchemy.ext.pylons.controller import _ModelsController as Base
from fa.jquery.wsgi import StaticApp
from fa.jquery.utils import TemplateEngine
from webhelpers.html import literal
from formalchemy.ext.pylons.controller import model_url
from formalchemy import fields
from routes.util import GenerationException
import renderers

class _ModelsController(Base):
    _static_app=StaticApp()
    engine = TemplateEngine()
    template = 'restfieldset.mako'

    def update_grid(self, *args, **kwargs):
        pass

def ModelsController(cls, prefix_name, member_name, collection_name):
    """wrap a controller with :class:~formalchemy.ext.pylons.controller._ModelsController"""
    return type(cls.__name__, (cls, _ModelsController),
                dict(prefix_name=prefix_name, member_name=member_name, collection_name=collection_name))

def RelationRenderer(renderer=fields.SelectFieldRenderer, **jq_options):
    class Renderer(renderer):
        def render(self, *args, **kwargs):
            html = super(Renderer, self).render(*args, **kwargs)
            fk_class = self.field.relation_type()
            model_name = fk_class.__name__
            try:
                field_url = '%s.xhr?field=%s' % (model_url('model', id=fields._pk(self.field.model)), self.field.key)
            except GenerationException:
                field_url = '%s.xhr?field=%s' % (model_url('new_model'), self.field.key)
            new_url = '%s.xhr' % model_url('new_model', model_name=model_name)
            html += literal('<button class="new_relation_item" alt="%s" href="%s">New %s</button>' % (
                                                field_url, new_url, model_name))
            return html
    return renderers.jQueryFieldRenderer('relation', show_input=True, renderer=Renderer, **jq_options)

renderers.default_renderers['dropdown'] = RelationRenderer()

