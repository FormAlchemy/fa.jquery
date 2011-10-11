from fanstatic import Library, Resource, Group
from js.jquery import jquery
from js.jqueryui import jqueryui, jqueryui_i18n
from js.jqueryui_syronex_colorpicker import colorpicker
from js.jqueryui_selectmenu import selectmenu
from js.jquery_markitup import markitup
from js.jquery_markitup import simple_style
from js.jquery_jgrowl import jquery_jgrowl
from js.tinymce import tinymce
from js.jqgrid import jqgrid
import os

fa_library = Library('fa', 'resources')

def R(path, *args, **kwargs):
    minified = os.path.join(fa_library.path, 'min', path)
    if os.path.isfile(minified):
        kwargs['minified'] = 'min/%s' % path
    return Resource(fa_library, path, *args, **kwargs)

fa_uiadmin_css = R("jquery.formalchemy.uiadmin.css")
fa_css = R("jquery.formalchemy.css")
fa_js = R("jquery.formalchemy.js",
          depends=[jquery, jqueryui, jqueryui_i18n])
fa_pyramid_js = R("jquery.pyramid_formalchemy.js", depends=[fa_js])

markitup_bbcode_set = R("markitup_sets/bbcode/set.js",
                        depends=[R("markitup_sets/bbcode/style.css"),
                                 fa_js, markitup, simple_style])
markitup_markdown_set = R("markitup_sets/markdown/set.js",
                          depends=[R("markitup_sets/markdown/style.css"),
                                   fa_js, markitup, simple_style])
markitup_textile_set = R("markitup_sets/textile/set.js",
                         depends=[R("markitup_sets/textile/style.css"),
                                  fa_js, markitup, simple_style])

jquery_tinymce = R("jquery.tinymce.js", depends=[tinymce, jquery])

fa_jqgrid = R('fa.jqgrid.js', depends=[jqgrid, fa_js])

fa = Group([fa_css, fa_js])
fa_admin = Group([fa_uiadmin_css, fa_css, fa_js, selectmenu])

