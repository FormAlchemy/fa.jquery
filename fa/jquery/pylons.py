# -*- coding: utf-8 -*-
from formalchemy.ext.pylons.controller import _ModelsController as Base
from fa.jquery.wsgi import StaticApp
from fa.jquery.utils import TemplateEngine
from webhelpers.html import literal
from formalchemy.ext.pylons.controller import model_url
from formalchemy.ext.pylons.controller import request
from formalchemy import fields
from routes.util import GenerationException
import renderers

class _ModelsController(Base):
    _static_app=StaticApp()
    engine = TemplateEngine()
    template = 'restfieldset.mako'

    def index(self, *args, **kwargs):
        kwargs['pager'] = ''
        return Base.index(self, *args, **kwargs)

    def get_page(self, **kwargs):
        if 'collection' not in kwargs:
            model = self.get_model()
            params = request.params
            session = self.Session()
            fields = model._descriptor._columns
            collection = session.query(model)
            sidx = params.get('sidx', getattr(model._descriptor, 'order_by') or 'id').decode()
            if sidx and hasattr(fields, sidx):
                sidx = getattr(fields, sidx)
                sord = params.get('sord', 'asc').decode().lower()
                if sord in ['asc', 'desc']:
                    collection = collection.order_by(getattr(sidx, sord)())
            kwargs.update(collection=collection)
        kwargs.update(items_per_page=int(request.GET.get('rows', 20)))
        return Base.get_page(self, **kwargs)

    def update_grid(self, *args, **kwargs):
        pass

    def get_filtered_ordered_queryset(self):
        model = self.get_model()
        params = request.params
        session = self.model.Session
        fields = model._descriptor._columns
        result = session.query(model)
        sidx = params.get('sidx', getattr(model._descriptor, 'order_by') or 'id').decode()
        if sidx and hasattr(fields, sidx):
            sidx = getattr(fields, sidx)
            sord = params.get('sord', 'asc').decode().lower()
            if sord in ['asc', 'desc']:
                result = result.order_by(getattr(sidx, sord)())
        return result

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

@renderers.alias(RelationRenderer, renderer=renderers.checkboxset())
def relations(): pass

@renderers.alias(RelationRenderer, renderer=renderers.radioset())
def relation(): pass

renderers.default_renderers['dropdown'] = RelationRenderer()

