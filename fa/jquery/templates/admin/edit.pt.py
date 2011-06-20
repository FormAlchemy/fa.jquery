registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _attrs_4365408720 = _loads('(dp1\nVname\np2\nVnext\np3\nsVvalue\np4\nV\nsVtype\np5\nVhidden\np6\nsVid\np7\nVnext\np8\ns.')
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_4365409424 = _loads('(dp1\nVclass\np2\nVfa_controls\np3\ns.')
    _attrs_4365406672 = _loads('(dp1\n.')
    _attrs_4365407632 = _loads('(dp1\n.')
    _attrs_4365408080 = _loads('(dp1\nVname\np2\nV_method\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nVPUT\np7\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4365407056 = _loads('(dp1\nVaction\np2\nV\nsVmethod\np3\nVPOST\np4\nsVenctype\np5\nVmultipart/form-data\np6\ns.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u'_init_stream()'
        (_out, _write, ) = _init_stream()
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        u"main.macros['master']"
        _metal = _lookup_attr(econtext['main'], 'macros')['master']
        def _callback_main(econtext, _repeat, _out=_out, _write=_write, _domain=_domain, **_ignored):
            if _repeat:
                repeat.update(_repeat)
            attrs = _attrs_4365406672
            _write(u'<div>\n      ')
            attrs = _attrs_4365407056
            u"''"
            _write(u'<form action="" method="POST" enctype="multipart/form-data">\n        ')
            _default.value = default = ''
            u'fs.render()'
            _content = _lookup_attr(econtext['fs'], 'render')()
            attrs = _attrs_4365407632
            u'_content'
            _write(u'<div>')
            _tmp1 = _content
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = str(_tmp)
                _write(_tmp)
            _write(u'</div>\n        ')
            attrs = _attrs_4365408080
            _write(u'<input type="hidden" name="_method" value="PUT" />\n        ')
            attrs = _attrs_4365408720
            u"u'\\n        '"
            _write(u'<input type="hidden" id="next" name="next" value="" />\n        ')
            _default.value = default = u'\n        '
            u'actions.buttons(request)'
            _content = _lookup_attr(econtext['actions'], 'buttons')(econtext['request'])
            attrs = _attrs_4365409424
            u'_content'
            _write(u'<div class="fa_controls">')
            _tmp1 = _content
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = str(_tmp)
                _write(_tmp)
            _write(u'</div>\n      </form>\n    </div>\n')
        u"{'main': _callback_main}"
        _tmp = {'main': _callback_main, }
        u"main.macros['master']"
        _metal.render(_tmp, _out=_out, _write=_write, _domain=_domain, econtext=econtext)
        return _out.getvalue()
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/fa.jquery/fa/jquery/templates/admin/edit.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
