registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _attrs_4357699984 = _loads('(dp1\nVid\np2\nVcontent\np3\nsVclass\np4\nVui-admin ui-widget\np5\ns.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4357699152 = _loads('(dp1\n.')
    _attrs_4357700560 = _loads('(dp1\n.')
    _attrs_4357698960 = _loads('(dp1\n.')
    _attrs_4357701584 = _loads('(dp1\nVsrc\np2\nVhttp://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/i18n/jquery-ui-i18n.min.js\np3\nsVtype\np4\nVtext/javascript\np5\ns.')
    _attrs_4357697872 = _loads('(dp1\nVtype\np2\nVtext/javascript\np3\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4357698384 = _loads('(dp1\n.')
    _attrs_4357701008 = _loads('(dp1\n.')
    _attrs_4357700944 = _loads('(dp1\nVstyle\np2\nVdisplay:none\np3\nsVclass\np4\nVroot_url\np5\ns.')
    _attrs_4357700496 = _loads('(dp1\nVid\np2\nVlanguages\np3\ns.')
    _attrs_4357698576 = _loads('(dp1\nVrel\np2\nVstylesheet\np3\ns.')
    _attrs_4357697680 = _loads('(dp1\nVtype\np2\nVtext/javascript\np3\ns.')
    _attrs_4357699408 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4357699344 = _loads('(dp1\nVid\np2\nVheader\np3\nsVclass\np4\nVui-widget-header ui-corner-all\np5\ns.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4357697808 = _loads('(dp1\n.')
    _marker = _loads("ccopy_reg\n_reconstructor\np1\n(cchameleon.core.i18n\nStringMarker\np2\nc__builtin__\nstr\np3\nS''\ntRp4\n.")
    _attrs_4357700432 = _loads('(dp1\nVstyle\np2\nVdisplay:none;\np3\nsVid\np4\nVmodels\np5\ns.')
    _attrs_4357701328 = _loads('(dp1\nVrel\np2\nVstylesheet\np3\ns.')
    _attrs_4357701072 = _loads('(dp1\nVclass\np2\nVbreadcrumb\np3\ns.')
    _attrs_4357701264 = _loads('(dp1\nVtype\np2\nVtext/javascript\np3\ns.')
    _attrs_4357701200 = _loads('(dp1\n.')
    _attrs_4357701136 = _loads('(dp1\nVtype\np2\nVtext/javascript\np3\ns.')
    _attrs_4357699856 = _loads('(dp1\n.')
    _attrs_4357701392 = _loads('(dp1\nVtype\np2\nVtext/css\np3\ns.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_4357698704 = _loads('(dp1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u"%(scope)s['%(out)s'], %(scope)s['%(write)s']"
        (_out, _write, ) = (econtext['_out'], econtext['_write'], )
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        attrs = _attrs_4357700560
        _write(u'<html>\n    ')
        attrs = _attrs_4357701008
        u"''"
        _write(u'<head>\n      ')
        _default.value = default = ''
        u'request.model_name'
        _tmp1 = _lookup_attr(econtext['request'], 'model_name')
        if _tmp1:
            pass
            u'request.model_name'
            _content = _lookup_attr(econtext['request'], 'model_name')
            attrs = _attrs_4357698704
            u'_content'
            _write(u'<title>')
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
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            _write(u'</title>')
        _write(u'\n      ')
        _tmp_domain0 = _domain
        u"u'fa_jquery'"
        _domain = u'fa_jquery'
        u'request.model_name is None'
        _tmp1 = (_lookup_attr(econtext['request'], 'model_name') is None)
        if _tmp1:
            pass
            attrs = _attrs_4357697808
            u"u'Models index'"
            _write(u'<title>')
            _msgid = u'Models index'
            u"%(translate)s(' '.join(%(msgid)s.split()), domain=%(domain)s, mapping=None, target_language=%(language)s, default=%(msgid)s)"
            _result = _translate(_lookup_attr(' ', 'join')(_msgid.split()), domain=_domain, mapping=None, target_language=target_language, default=_msgid)
            u'_result'
            _tmp1 = _result
            _write((_tmp1 + u'</title>'))
        _write(u'\n      ')
        _domain = _tmp_domain0
        attrs = _attrs_4357698576
        u"request.static_url('fa.jquery:jquery-ui/css/smoothness/jquery-ui-1.8.8.custom.css')"
        _write(u'<link rel="stylesheet"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('fa.jquery:jquery-ui/css/smoothness/jquery-ui-1.8.8.custom.css')
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u' />\n      ')
        attrs = _attrs_4357701328
        u"request.static_url('fa.jquery:jquery-ui/fa.jquery.min.css')"
        _write(u'<link rel="stylesheet"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('fa.jquery:jquery-ui/fa.jquery.min.css')
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u' />\n      ')
        attrs = _attrs_4357697680
        u"request.static_url('fa.jquery:jquery-ui/fa.jquery.min.js')"
        _write(u'<script type="text/javascript"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('fa.jquery:jquery-ui/fa.jquery.min.js')
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' src="' + _tmp1) + '"'))
        _write(u'></script>\n      ')
        attrs = _attrs_4357701584
        _write(u'<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/i18n/jquery-ui-i18n.min.js"></script>\n      ')
        attrs = _attrs_4357697872
        u"request.static_url('fa.jquery:jquery-ui/fa/jquery.pyramid_formalchemy.js')"
        _write(u'<script type="text/javascript"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('fa.jquery:jquery-ui/fa/jquery.pyramid_formalchemy.js')
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' src="' + _tmp1) + '"'))
        _write(u'></script>\n      ')
        attrs = _attrs_4357701136
        u"%(slots)s.get(u'javascript')"
        _write(u'<script type="text/javascript">\n        jQuery(document).ready(function() {\n          $(\'select#models\')\n            .change(function() { window.location.href = $(this).val(); })\n            .selectmenu({\'style\':\'dropdown\', \'menuWidth\':\'20%\', \'width\':\'100%\'});\n        });\n      </script>\n      ')
        _tmp = _slots.get(u'javascript')
        u'%(tmp)s is not None'
        _tmp1 = (_tmp is not None)
        if _tmp1:
            pass
            u'isinstance(%(tmp)s, basestring)'
            _tmp2 = isinstance(_tmp, basestring)
            if not _tmp2:
                pass
                econtext.update(dict(rcontext=rcontext, _domain=_domain))
                _tmp(econtext, repeat)
            else:
                pass
                u'%(tmp)s'
                _tmp2 = _tmp
                _tmp = _tmp2
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
        else:
            pass
            attrs = _attrs_4357701264
            _write(u'<script type="text/javascript"></script>')
        _write(u'\n      ')
        attrs = _attrs_4357701392
        _write(u'<style type="text/css">\n        label {font-weight:bold;}\n        h1, h3 {padding:0.1 0.3em;}\n        h1 a, h3 a {text-decoration:none;}\n        #header { height: 2em; font-size:1.5em; }\n        #header div { font-size:1.5em; }\n        #header a { font-size:1em; }\n        ul#languages {float:right;}\n        ul#languages li {display: inline;}\n        ul#languages a {text-decoration:none; color: grey;}\n        ul#languages a.lang_active {text-decoration:underline;}\n        div.breadcrumb {float:right;width:20%;margin-right:20px;}\n        div.breadcrumb a {text-decoration:none;}\n        h1 a.ui-selectmenu {height:1em;}\n        a.ui-state-default {padding:0.1em 0.3em;}\n        a.fm-button {padding:0.4em 0.5em;}\n        a.fm-button-icon-left {padding-left:1.9em;}\n      </style>\n    </head>\n    ')
        attrs = _attrs_4357699152
        _write(u'<body>\n      ')
        attrs = _attrs_4357699984
        _write(u'<div id="content" class="ui-admin ui-widget">\n        ')
        attrs = _attrs_4357699344
        u'request.model_name and breadcrumb'
        _write(u'<h1 id="header" class="ui-widget-header ui-corner-all">\n          ')
        _tmp1 = (_lookup_attr(econtext['request'], 'model_name') and econtext['breadcrumb'])
        if _tmp1:
            pass
            attrs = _attrs_4357701072
            _write(u'<div class="breadcrumb">\n            ')
            _tmp_domain1 = _domain
            u"u'fa_jquery'"
            _domain = u'fa_jquery'
            attrs = _attrs_4357700432
            u'breadcrumb'
            _write(u'<select id="models" style="display:none;">\n            ')
            _tmp1 = econtext['breadcrumb']
            item = None
            (_tmp1, _tmp2, ) = repeat.insert('item', _tmp1)
            for item in _tmp1:
                _tmp2 = (_tmp2 - 1)
                u"''"
                _write(u'')
                _default.value = default = ''
                u'item[1]'
                _content = item[1]
                attrs = _attrs_4357698960
                u'item[0]'
                _write(u'<option')
                _tmp3 = item[0]
                if (_tmp3 is _default):
                    _tmp3 = None
                if ((_tmp3 is not None) and (_tmp3 is not False)):
                    if (_tmp3.__class__ not in (str, unicode, int, float, )):
                        _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                    else:
                        if not isinstance(_tmp3, unicode):
                            _tmp3 = str(_tmp3)
                    if ('&' in _tmp3):
                        if (';' in _tmp3):
                            _tmp3 = _re_amp.sub('&amp;', _tmp3)
                        else:
                            _tmp3 = _tmp3.replace('&', '&amp;')
                    if ('<' in _tmp3):
                        _tmp3 = _tmp3.replace('<', '&lt;')
                    if ('>' in _tmp3):
                        _tmp3 = _tmp3.replace('>', '&gt;')
                    if ('"' in _tmp3):
                        _tmp3 = _tmp3.replace('"', '&quot;')
                    _write(((' value="' + _tmp3) + '"'))
                u' item[2]'
                _tmp3 = item[2]
                if (_tmp3 is _default):
                    _tmp3 = None
                if ((_tmp3 is not None) and (_tmp3 is not False)):
                    if (_tmp3.__class__ not in (str, unicode, int, float, )):
                        _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                    else:
                        if not isinstance(_tmp3, unicode):
                            _tmp3 = str(_tmp3)
                    if ('&' in _tmp3):
                        if (';' in _tmp3):
                            _tmp3 = _re_amp.sub('&amp;', _tmp3)
                        else:
                            _tmp3 = _tmp3.replace('&', '&amp;')
                    if ('<' in _tmp3):
                        _tmp3 = _tmp3.replace('<', '&lt;')
                    if ('>' in _tmp3):
                        _tmp3 = _tmp3.replace('>', '&gt;')
                    if ('"' in _tmp3):
                        _tmp3 = _tmp3.replace('"', '&quot;')
                    _write(((' class="' + _tmp3) + '"'))
                u'_content'
                _write('>')
                _tmp3 = _content
                _tmp = _tmp3
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
                    if ('&' in _tmp):
                        if (';' in _tmp):
                            _tmp = _re_amp.sub('&amp;', _tmp)
                        else:
                            _tmp = _tmp.replace('&', '&amp;')
                    if ('<' in _tmp):
                        _tmp = _tmp.replace('<', '&lt;')
                    if ('>' in _tmp):
                        _tmp = _tmp.replace('>', '&gt;')
                    _write(_tmp)
                _write(u'</option>\n            ')
                if (_tmp2 == 0):
                    break
                _write(' ')
            _write(u'\n            </select>\n          ')
            _domain = _tmp_domain1
            _write(u'</div>')
        u'request.model_name'
        _write(u'\n          ')
        _tmp1 = _lookup_attr(econtext['request'], 'model_name')
        if _tmp1:
            pass
            attrs = _attrs_4357701200
            u"''"
            _write(u'<div>\n            ')
            _default.value = default = ''
            u'model_name'
            _content = econtext['model_name']
            attrs = _attrs_4357699856
            u'request.fa_url(model_name)'
            _write(u'<a')
            _tmp1 = _lookup_attr(econtext['request'], 'fa_url')(econtext['model_name'])
            if (_tmp1 is _default):
                _tmp1 = None
            if ((_tmp1 is not None) and (_tmp1 is not False)):
                if (_tmp1.__class__ not in (str, unicode, int, float, )):
                    _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp1, unicode):
                        _tmp1 = str(_tmp1)
                if ('&' in _tmp1):
                    if (';' in _tmp1):
                        _tmp1 = _re_amp.sub('&amp;', _tmp1)
                    else:
                        _tmp1 = _tmp1.replace('&', '&amp;')
                if ('<' in _tmp1):
                    _tmp1 = _tmp1.replace('<', '&lt;')
                if ('>' in _tmp1):
                    _tmp1 = _tmp1.replace('>', '&gt;')
                if ('"' in _tmp1):
                    _tmp1 = _tmp1.replace('"', '&quot;')
                _write(((' href="' + _tmp1) + '"'))
            u'_content'
            _write('>')
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
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            u"''"
            _write(u'</a>\n            ')
            _default.value = default = ''
            u"request.model_id and hasattr(request.model_class, '__unicode__')"
            _tmp1 = (_lookup_attr(econtext['request'], 'model_id') and hasattr(_lookup_attr(econtext['request'], 'model_class'), '__unicode__'))
            if _tmp1:
                pass
                u'unicode(request.model_instance)'
                _content = unicode(_lookup_attr(econtext['request'], 'model_instance'))
                u'_content'
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
                    if ('&' in _tmp):
                        if (';' in _tmp):
                            _tmp = _re_amp.sub('&amp;', _tmp)
                        else:
                            _tmp = _tmp.replace('&', '&amp;')
                    if ('<' in _tmp):
                        _tmp = _tmp.replace('<', '&lt;')
                    if ('>' in _tmp):
                        _tmp = _tmp.replace('>', '&gt;')
                    _write(_tmp)
            u"''"
            _write(u'\n            ')
            _default.value = default = ''
            u"request.model_id and not hasattr(request.model_class, '__unicode__')"
            _tmp1 = (_lookup_attr(econtext['request'], 'model_id') and not hasattr(_lookup_attr(econtext['request'], 'model_class'), '__unicode__'))
            if _tmp1:
                pass
                u'request.model_id'
                _content = _lookup_attr(econtext['request'], 'model_id')
                u'_content'
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
                    if ('&' in _tmp):
                        if (';' in _tmp):
                            _tmp = _re_amp.sub('&amp;', _tmp)
                        else:
                            _tmp = _tmp.replace('&', '&amp;')
                    if ('<' in _tmp):
                        _tmp = _tmp.replace('<', '&lt;')
                    if ('>' in _tmp):
                        _tmp = _tmp.replace('>', '&gt;')
                    _write(_tmp)
            _write(u'\n          </div>')
        _write(u'\n          ')
        _tmp_domain0 = _domain
        u"u'fa_jquery'"
        _domain = u'fa_jquery'
        u'not request.model_name'
        _tmp1 = not _lookup_attr(econtext['request'], 'model_name')
        if _tmp1:
            pass
            attrs = _attrs_4357698384
            u"u'Models index'"
            _write(u'<div>')
            _msgid = u'Models index'
            u"%(translate)s(' '.join(%(msgid)s.split()), domain=%(domain)s, mapping=None, target_language=%(language)s, default=%(msgid)s)"
            _result = _translate(_lookup_attr(' ', 'join')(_msgid.split()), domain=_domain, mapping=None, target_language=target_language, default=_msgid)
            u'_result'
            _tmp1 = _result
            _write((_tmp1 + u'</div>'))
        _write(u'\n        ')
        _domain = _tmp_domain0
        u"%(slots)s.get(u'main')"
        _write(u'</h1>\n        ')
        _tmp = _slots.get(u'main')
        u'%(tmp)s is not None'
        _tmp1 = (_tmp is not None)
        if _tmp1:
            pass
            u'isinstance(%(tmp)s, basestring)'
            _tmp2 = isinstance(_tmp, basestring)
            if not _tmp2:
                pass
                econtext.update(dict(rcontext=rcontext, _domain=_domain))
                _tmp(econtext, repeat)
            else:
                pass
                u'%(tmp)s'
                _tmp2 = _tmp
                _tmp = _tmp2
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
        else:
            pass
            attrs = _attrs_4357699408
            _write(u'<div>\n        </div>')
        u"''"
        _write(u'\n        ')
        _default.value = default = ''
        u'request'
        _tmp1 = econtext['request']
        if _tmp1:
            pass
            u'request.language_actions.render(request)'
            _content = _lookup_attr(_lookup_attr(econtext['request'], 'language_actions'), 'render')(econtext['request'])
            attrs = _attrs_4357700496
            u'_content'
            _write(u'<ul id="languages">')
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
            _write(u'</ul>')
        _write(u'\n        ')
        attrs = _attrs_4357700944
        u'request.fa_url()'
        _write(u'<a style="display:none" class="root_url"')
        _tmp1 = _lookup_attr(econtext['request'], 'fa_url')()
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u'></a>\n      </div>\n    </body>\n</html>')
        return
    return render

__filename__ = '/Users/gawel/py/formalchemy_project/fa.jquery/fa/jquery/templates/admin/master.pt'
registry[('master', False, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
