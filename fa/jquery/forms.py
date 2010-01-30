# -*- coding: utf-8 -*-
from simplejson import dumps
from utils import templates

class Tabs(object):
    """Display FieldSet using http://jqueryui.com/demos/tabs/:

    .. sourcecode:: python

        >>> from testing import *
        >>> tabs = Tabs('my_tabs',
        ...             ('tab1', 'My first tab', fs1),
        ...             footer='<input type="submit" name="%(id)s" />')
        >>> tabs.append('tab2', 'The second', fs2)
        >>> tabs.tab1 = tabs.tab1.bind(obj1)
        >>> tabs.bind(obj2, tabs.tab2)
        >>> print tabs.render(selected=2) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div id="my_tabs">
        <ul>
            <li><a href="#tab1">My first tab</a></li>
            <li><a href="#tab2">The second</a></li>
        </ul>
        <div id="tab1">...
        </div>
        <div id="tab2">...
        </div>
        </div>
        <script type="text/javascript">
          jQuery.fa.tabs('my_tabs', {"selected": 2});
        </script>
        <BLANKLINE>
            
    """
    template = templates.get_template('/forms/tabs.mako')
    def __init__(self, id, *fieldsets, **options):
        if not isinstance(id, basestring):
            raise TypeError('id must be a string. got %r' % (id,))
        self._id = id
        self._fs = []
        self._fs_dict = {}
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

    @property
    def model(self):
        if self._fs:
            return self._fs[0].model

    def __getattr__(self, attr):
        return self._fs_dict.get(attr)

    def __setattr__(self, attr, fs):
        if attr.startswith('_'):
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

    def bind(self, model, *ids, **kwargs):
        """Bind fieldsets to model.  If no ids is provided, all fieldsets are
        bound to model. Session and data can be passed as kwargs."""
        ids = ids or self._fs_dict.keys()
        for id in ids:
            fs = self.get(id)
            id = fs.__name__
            fs = fs.bind(model, **kwargs)
            fs.__name__ = id
            self._fs_dict[id] = fs

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
                                    fieldsets=fieldsets,
                                    submit=self._submit,
                                    options=dumps(options),
                                    **kwargs)

class Accordion(Tabs):
    """Work like :class:`~fa.jquery.forms.Tabs` but use
    http://jqueryui.com/demos/accordion/
    """
    template = templates.get_template('/forms/accordion.mako')
