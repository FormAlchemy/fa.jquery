# -*- coding: utf-8 -*-
from formalchemy.i18n import get_translator
from formalchemy.fields import _pk
from simplejson import dumps
from utils import templates
from random import random

class MultiFieldSetProperty(property):

    def __init__(self, name):
        self.__name__ = '_' + name

    def __get__(self, instance, klass):
        if instance is None:
            return klass
        return getattr(instance, self.__name__)

    def __set__(self, instance, value):
        setattr(instance, self.__name__, value)
        for fs in instance._fs_dict.values():
            setattr(fs, self.__name__[1:], value)

class MultiFieldSet(object):
    """Display more than one FieldSet:

    .. sourcecode:: python

        >>> from testing import *
        >>> fs = MultiFieldSet('my_fieldsets',
        ...             ('fs1', '', fs1))
        >>> fs.append('fs2', 'Second fieldset', fs2)
        >>> fs.fs1 = fs.fs1.bind(obj1)
        >>> fs.fs2.rebind(obj2)
        >>> print fs.render() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div id="my_fieldsets_...">
        <fieldset id="fs1_...">
        <div>
        ...
        </div>
        </fieldset>
        <fieldset id="fs2_...">
        <legend><a href="#fs2_...">Second fieldset</a></legend>
        <div>
        ...

    """
    template = templates.get_template('/forms/multifieldset.mako')
    def __init__(self, id, *fieldsets, **options):
        if not isinstance(id, basestring):
            raise TypeError('id must be a string. got %r' % (id,))
        self._id = id
        self._fs = []
        self._fs_dict = {}
        self.__bound_pk = None
        self.__request = None
        self._options = options
        self._readonly = False
        self._engine = None
        self._focus = False
        self._original_cls = None
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

    _bound_pk = MultiFieldSetProperty('_bound_pk')
    _request = MultiFieldSetProperty('_request')
    focus = MultiFieldSetProperty('focus')
    engine = MultiFieldSetProperty('engine')
    readonly = MultiFieldSetProperty('readonly')

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

    def append(self, id, title, fs):
        """add a fieldset to tabs"""
        fs.__name__ = id
        self._fs.append((id, title))
        self._fs_dict[id] = fs

    def get(self, fs):
        if isinstance(fs, basestring):
            fs = self._fs_dict[fs]
        return fs

    def bind(self, model=None, **kwargs):
        """Bind fieldsets to model. All sub-fieldsets are bound to model."""
        news = []
        for id, title in self._fs:
            fs = self.get(id)
            fs = fs.bind(model=model, **kwargs)
            if model is None:
                model = fs.model
            news.append((id, title, fs))
        return self.__class__(self._id, *news, **self._options.copy())

    def rebind(self, model=None, **kwargs):
        """Bind fieldsets to model. All sub-fieldsets are bound to model."""
        for id, title in self._fs:
            fs = self.get(id)
            fs.rebind(model=model, **kwargs)
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
        return self.template.render_unicode(id=self._id,
                                    rid=str(random())[2:],
                                    fieldsets=fieldsets,
                                    options=dumps(options),
                                    F_=get_translator(request=self.__request),
                                    **kwargs)


class Tabs(MultiFieldSet):
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
    template = templates.get_template('/forms/tabs.mako')

class Accordion(MultiFieldSet):
    """Work like :class:`~fa.jquery.forms.Tabs` but use
    http://jqueryui.com/demos/accordion/
    """
    template = templates.get_template('/forms/accordion.mako')

