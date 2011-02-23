# -*- coding: utf-8 -*-
from pyramid_formalchemy.views import ModelView as Base
from pyramid_formalchemy.utils import TemplateEngine
from fa.jquery import utils
from webhelpers.html import literal
from formalchemy import fields
from formalchemy import fatypes
from simplejson import dumps
import renderers
import logging

class ModelView(Base):

    engine = TemplateEngine()

    def index(self, *args, **kwargs):
        kwargs['pager'] = ''
        return Base.index(self, *args, **kwargs)

    def get_page(self, **kwargs):
        if 'collection' not in kwargs:
            model = self.get_model()
            params = self.request.params
            session = self.Session()
            fields = model._sa_class_manager
            collection = session.query(model)
            # FIXME: use id by default but should use pk field
            sidx = params.get('sidx', 'id').decode()
            if sidx and fields.has_key(sidx):
                sidx = fields[sidx]
                sord = params.get('sord', 'asc').decode().lower()
                if sord in ['asc', 'desc']:
                    collection = collection.order_by(getattr(sidx, sord)())
            if 'searchField' in params:
                field = fields.get(params['searchField'], None)
                if field:
                    op = params['searchOper']
                    value = params['searchString']
                    if op == 'cn':
                        value = '%%%s%%' % value
                        filter = field.ilike(value)
                    else:
                        filter = field==value
                    collection = collection.filter(filter)
            kwargs.update(collection=collection)
        if 'items_per_page' not in kwargs:
            kwargs.update(items_per_page=int(self.request.GET.get('rows', 20)))
        return Base.get_page(self, **kwargs)

    def render_xhr_format(self, fs=None, **kwargs):
        resp = Base.render_xhr_format(self, fs=fs, **kwargs)
        if fs and self.request.POST and 'field' not in self.request.GET:
            flash = utils.Flash()
            if fs.errors:
                errors = [f.label_text or fs.prettify(f.key) for f in fs.render_fields.values() if f.errors]
                flash.error('Field(s) %s have errors' % ','.join(errors))
            else:
                flash.info('Record saved')
            resp.unicode_body += flash.render()
        return resp

    def update_grid(self, grid, *args, **kwargs):
        metadatas = ('width', 'align', 'fixed', 'search', 'stype', 'searchoptions')
        for field in grid.render_fields.values():
            metadata = dict(search=0, sortable=1, id=field.key, name=field.key)
            searchoptions = dict(sopt=['eq', 'cn'])
            if field.is_relation:
                metadata.update(width=100, sortable=0)
            elif isinstance(field.type, (utils.Color, utils.Slider)):
                metadata.update(width=50, align='center')
            elif isinstance(field.type, fatypes.Text):
                field.set(renderer=renderers.ellipsys(field.renderer))
                metadata.update(search=1)
            elif isinstance(field.type, (fatypes.String, fatypes.Unicode)):
                metadata.update(search=1)
            elif isinstance(field.type, (fatypes.Date, fatypes.Integer)):
                metadata.update(width=70, align='center')
            elif isinstance(field.type, fatypes.DateTime):
                metadata.update(width=120, align='center')
            elif isinstance(field.type, fatypes.Boolean):
                metadata.update(width=30, align='center')
            if metadata['search']:
                metadata['searchoptions'] = searchoptions
            metadata = dict(json=dumps(metadata))
            field.set(metadata=metadata)

#def RelationRenderer(renderer=fields.SelectFieldRenderer, **jq_options):
#    class Renderer(renderer):
#        def render(self, *args, **kwargs):
#            html = super(Renderer, self).render(*args, **kwargs)
#            fk_class = self.field.relation_type()
#            model_name = fk_class.__name__
#            try:
#                field_url = '%s.xhr?field=%s' % (model_url('model', id=fields._pk(self.field.model)), self.field.key)
#            except GenerationException:
#                field_url = '%s.xhr?field=%s' % (model_url('new_model'), self.field.key)
#            new_url = '%s.xhr' % model_url('new_model', model_name=model_name)
#            html += literal('<button class="new_relation_item" alt="%s" href="%s">New %s</button>' % (
#                                                field_url, new_url, model_name))
#            return html
#    return renderers.jQueryFieldRenderer('relation', show_input=True, renderer=Renderer, **jq_options)

#@renderers.alias(RelationRenderer, renderer=renderers.checkboxset())
#def relations(): pass

#@renderers.alias(RelationRenderer, renderer=renderers.radioset())
#def relation(): pass

#renderers.default_renderers['dropdown'] = RelationRenderer()

