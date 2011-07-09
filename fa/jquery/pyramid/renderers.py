# -*- coding: utf-8 -*-
from formalchemy import fields
from formalchemy import helpers as h
from webhelpers.html import literal
from fa.jquery import renderers
from fa.jquery import fanstatic_resources

def RelationRenderer(renderer=fields.SelectFieldRenderer, **jq_options):
    class Renderer(renderer):
        def render(self, *args, **kwargs):
            html = super(Renderer, self).render(*args, **kwargs)
            pk = fields._pk(self.field.model)
            model_name = self.field.parent.model.__class__.__name__
            request = self.request
            if pk:
                field_url = request.fa_url(model_name, 'xhr', pk, field=self.field.key)
            else:
                field_url = request.fa_url(model_name, 'xhr', field=self.field.key)
            fk_class = self.field.relation_type()
            model_name = fk_class.__name__
            new_url = request.fa_url(model_name, 'xhr', 'new')
            html += literal('<button class="new_relation_item" alt="%s" href="%s">New %s</button>' % (
                                                field_url, new_url, model_name))
            return html
    return renderers.jQueryFieldRenderer('relation', show_input=True, renderer=Renderer, **jq_options)

@renderers.alias(RelationRenderer, renderer=renderers.checkboxset())
def relations(): pass

@renderers.alias(RelationRenderer, renderer=renderers.radioset())
def relation(): pass

def AutocompleteRelationRenderer(filter_by='id', renderer=fields.IntegerFieldRenderer, **jq_options):
    """Use http://docs.jquery.com/UI/Autocomplete with pyramid"""

    class Renderer(renderer):

        def __init__(self, *args, **kwargs):
            super(Renderer, self).__init__(*args, **kwargs)
            self.field.render_opts['options'] = []

        def update_options(self, options, kwargs):
            kwargs['source'] = self.request.fa_url(
                    self.field.relation_type().__name__, 'autocomplete')

        def render(self, **kwargs):
            fanstatic_resources.fa_pyramid_js.need()
            filter_by = self.jq_options.get('filter_by')
            if self.raw_value:
                label = getattr(self.raw_value, filter_by, u'Not selected')
            else:
                label = u''

            html = h.radio_button(self.name, value=self.value, **kwargs)
            html += h.label(label)

            return ''.join(html)

    jq_options.update(filter_by=filter_by, show_input=False)

    return renderers.jQueryFieldRenderer('autocomplete_relation', renderer=Renderer, **jq_options)

@renderers.alias(AutocompleteRelationRenderer)
def autocomplete_relation(): pass
