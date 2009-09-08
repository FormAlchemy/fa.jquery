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
        >>> tabs.bind(obj2, 'tab2')
        >>> print tabs.render(selected=2) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <div id="my_tabs">
        <ul>
            <li><a href="#tab1">My first tab</a></li>
            <li><a href="#tab2">The second</a></li>
        </ul>
        <div id="tab1">...
            <div>
              <label class="field_req" for="Tab1--title">title</label>
              <input id="Tab1--title" name="Tab1--title" type="text" />
            </div>...
            <input type="submit" name="tab1" />
        </div>
        <div id="tab2">...
            <input type="submit" name="tab2" />
        </div>
        </div>
        <script type="text/javascript">
          jQuery('#my_tabs').tabs({"selected": 2});
        </script>
        <BLANKLINE>
            
    """
    template = templates.get_template('tabs.mako')
    def __init__(self, id, *forms, **options):
        if not isinstance(id, basestring):
            raise TypeError('id must be a string. got %r' % (id,))
        self._id = id
        self._fs = []
        self._fs_dict = {}
        self._options = options
        for form in forms:
            if not isinstance(form, (tuple, list)) or len(form) != 3:
                raise ValueError('A form is defined by (id, title, form) got %r' % (form,))
            self.append(*form)

    def __getattr__(self, attr):
        return self._fs_dict.get(attr)

    def __setattr__(self, attr, form):
        if attr.startswith('_'):
            object.__setattr__(self, attr, form)
        else:
            self._fs_dict[attr] = form

    def append(self, id, title, fs):
        """add a fieldset to tabs"""
        self._fs.append((id, title))
        self._fs_dict[id] = fs

    def bind(self, model, *ids, **kwargs):
        """Bind forms to model.  If no ids is provided, all forms are bound to
        model. Session and data can be passed as kwargs."""
        ids = ids or self._fs_dict.keys()
        for id in ids:
            fs = self._fs_dict[id]
            self._fs_dict[id] = fs.bind(model, **kwargs)

    def validate(self, *ids):
        """Validate forms. If no ids is provided, all forms are validate."""
        forms = []
        ids = ids or self._fs_dict.keys()
        for id in ids:
            forms.append(self._fs_dict[id])
        validated = [fs.validate() for fs in forms]
        if False in validated:
            return False
        return True

    def sync(self, *ids):
        """Sync forms. If no ids is provided, all forms are validate."""
        ids = ids or self._fs_dict.keys()
        for id in ids:
            self._fs_dict[id].sync()

    def render(self, *ids, **options):
        forms = []
        ids = ids or self._fs_dict.keys()
        for id, title in self._fs:
            if id in ids:
                fs = self._fs_dict[id]
                fs.focus = False
                forms.append(dict(id=id, title=title, fs=fs))
        kwargs = dict(footer='', header='')
        kwargs.update(self._options)
        return self.template.render(id=self._id,
                                    forms=forms,
                                    submit=self._submit,
                                    options=options and dumps(options) or '',
                                    **kwargs)

