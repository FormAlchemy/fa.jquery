# -*- coding: utf-8 -*-
from formalchemy.fields import _pk
from simplejson import dumps
from utils import templates
from random import random

class Tabs(object):
    """Display FieldSet using http://jqueryui.com/demos/tabs/:

    .. sourcecode:: python

        >>> from testing import *
        >>> tabs = Tabs('my_tabs',
        ...             ('tab1', 'My first tab', fs1),
        ...             footer='<input type="submit" name="%(id)s" />')
        >>> tabs.append('tab2', 'The second', fs2)
        >>> tabs.tab1 = tabs.tab1.bind(obj1)
        >>> tabs.tab2.rebind(obj2)
        >>> print tabs.render(selected=2) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div id="my_tabs_...">
        <ul>
            <li><a href="#tab1_...">My first tab</a></li>
            <li><a href="#tab2_...">The second</a></li>
        </ul>
        <div id="tab1_...">...
        </div>
        <div id="tab2_...">...
        </div>
        </div>
        <script type="text/javascript">
          jQuery.fa.tabs('my_tabs_...', {"selected": 2});
        </script>
        <BLANKLINE>
            
    """
    engine = None
    template = templates.get_template('/forms/tabs.mako')
    def __init__(self, id, *fieldsets, **options):
        if not isinstance(id, basestring):
            raise TypeError('id must be a string. got %r' % (id,))
        self._id = id
        self._fs = []
        self._fs_dict = {}
        self._bound_pk = None
        self._options = options
        for fs in fieldsets:
            if not isinstance(fs, (tuple, list)) or len(fs) != 3:
                raise ValueError('A form is defined by (id, title, form) got %r' % (fs,))
            self.append(*fs)

    def jsonify(self):
        fields = []
        for fs in self._fs:
            for f in fs.render_fields.values():
                fields.append((f.key, f.model_value))
        return dict(fields)

    def _get_bound_pk(self):
        for fs in self._fs:
            return fs._bound_pk

    def _set_bound_pk(self, value):
        for fs in self._fs:
            fs._bound_pk = value

    _bound_pk = property(_get_bound_pk, _set_bound_pk)

    @property
    def model(self):
        if self._fs:
            return self._fs_dict.get(self._fs[0][0]).model

    @property
    def errors(self):
        errors = {}
        for fs in self._fs_dict.values():
            errors.update(fs.errors)
        return errors

    @property
    def render_fields(self):
        fields = {}
        for fs in self._fs_dict.values():
            fields.update(fs.render_fields)
        return fields

    def __getattr__(self, attr):
        if attr in self._fs_dict:
            return self._fs_dict.get(attr)
        else:
            raise AttributeError(attr)

    def __setattr__(self, attr, fs):
        if attr.startswith('_') or attr in ('engine', 'readonly'):
            object.__setattr__(self, attr, fs)
        else:
            fs.__name__ = attr
            self._fs_dict[attr] = fs

    def append(self, id, title, fs):
        """add a fieldset to tabs"""
        fs.__name__ = id
        self._fs.append((id, title))
        self._fs_dict[id] = fs

    def get(self, fs):
        if isinstance(fs, basestring):
            fs = self._fs_dict[fs]
        return fs

    def bind(self, model=None, session=None, data=None):
        """Bind fieldsets to model. All sub-fieldsets are bound to model."""
        news = []
        for id, title in self._fs:
            fs = self.get(id)
            fs = fs.bind(model=model, data=data, session=session)
            if model is None:
                model = fs.model
            news.append((id, title, fs))
        return self.__class__(self._id, *news, **self._options.copy())

    def rebind(self, model=None, session=None, data=None):
        """Bind fieldsets to model. All sub-fieldsets are bound to model."""
        for id, title in self._fs:
            fs = self.get(id)
            fs.rebind(model=model, data=data, session=session)
            if model is None:
                model = fs.model

    def copy(self):
        news = []
        for id, title in self._fs:
            fs = self.get(id)
            fs = fs.bind(model=fs.model)
            news.append((id, title, fs))
        return self.__class__(self._id, *news, **self._options.copy())

    def validate(self, *ids):
        """Validate fieldsets. If no ids is provided, all fieldsets are
        validate."""
        fieldsets = []
        ids = ids or self._fs_dict.keys()
        for id in ids:
            fieldsets.append(self.get(id))
        validated = [fs.validate() for fs in fieldsets]
        if False in validated:
            return False
        return True

    def sync(self, *ids):
        """Sync fieldsets. If no ids is provided, all fieldsets are
        validate."""
        ids = ids or self._fs_dict.keys()
        for id in ids:
            self.get(id).sync()

    def render(self, *ids, **options):
        fieldsets = []
        if ids:
            ids = [self.get(id).__name__ for id in ids]
        else:
            ids = self._fs_dict.keys()
        for id, title in self._fs:
            if id in ids:
                fs = self._fs_dict[id]
                fs.focus = False
                fieldsets.append(dict(id=id, title=title, fs=fs))
        kwargs = dict(footer='', header='')
        kwargs.update(self._options)
        return self.template.render(id=self._id,
                                    rid=str(random())[2:],
                                    fieldsets=fieldsets,
                                    options=dumps(options),
                                    **kwargs)

class Accordion(Tabs):
    """Work like :class:`~fa.jquery.forms.Tabs` but use
    http://jqueryui.com/demos/accordion/
    """
    template = templates.get_template('/forms/accordion.mako')
