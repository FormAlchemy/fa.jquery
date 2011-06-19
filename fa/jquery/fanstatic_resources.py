from fanstatic import Library, Resource, Group
from js.jquery import jquery
from js.jqueryui_syronex_colorpicker import colorpicker
from js.jquery_markitup import simple_style
from js.jqgrid import jqgrid

fa_library = Library('fa', 'jquery-ui')

R = lambda x: Resource(fa_library, x)

fa_js = Resource(fa_library, "fa/jquery.formalchemy.js",
                 depends=[jquery, colorpicker])
fa_css = R("fa/jquery.formalchemy.css")
fa_globals_css = R("css/global.css")

fa = Group([fa_js, fa_css, fa_globals_css])

markitup_bbcode_set = Resource(fa_library, "markitup_sets/bbcode/set.js",
                               depends=[R("markitup_sets/bbcode/style.css"),
                                        fa_js, simple_style])
markitup_markdown_set = Resource(fa_library, "markitup_sets/markdown/set.js",
                                 depends=[R("markitup_sets/markdown/style.css"),
                                          fa_js, simple_style])
markitup_textile_set = Resource(fa_library, "markitup_sets/textile/set.js",
                                depends=[R("markitup_sets/textile/style.css"),
                                         fa_js, simple_style])

fa_jqgrid = Resource(fa_library, 'fa/fa.jqgrid.js',
                     depends=[jqgrid, fa])
