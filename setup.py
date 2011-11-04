from setuptools import setup, find_packages

version = '0.9.5'

long_description = open("README.txt").read()
long_description += """
CHANGES
==========
"""
long_description += open("CHANGES.txt").read()

setup(name='fa.jquery',
      version=version,
      description="jQuery widgets for formalchemy",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='jquery ajax widgets',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='http://docs.formalchemy.org/fa.jquery/index.html',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fa'],
      message_extractors = { 'fa/jquery': [
             ('*.py', 'lingua_python', None ),
             ('templates/**.pt', 'chameleon_xml', None ),
             ]},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'FormAlchemy',
          'WebHelpers',
          'simplejson',
          'textile',
          'postmarkup',
          'markdown',
          'fanstatic',
          'js.jquery',
          'js.jquery_form',
          'js.jquery_markitup',
          'js.jqueryui',
          'js.jqueryui_selectmenu',
          'js.jqueryui_syronex_colorpicker',
          'js.jquery_jgrowl',
          'js.tinymce',
          'js.jqgrid',
          'mako',
          'Babel',
      ],
      entry_points="""
      [paste.app_factory]
      main = fa.jquery.wsgi:StaticApp
      test = fa.jquery.app:make_app
      [paste.filter_factory]
      demo = fa.jquery.app:make_demo
      [fanstatic.libraries]
      fa = fa.jquery.fanstatic_resources:fa_library
      """,
      )
