import sys
import os

from mo import __version__


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'M-O'
copyright = '2016, Thomas Leese'
author = 'Thomas Leese'

version = __version__
release = __version__

language = None

exclude_patterns = ['_build']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'M-Odoc'

intersphinx_mapping = {'https://docs.python.org/': None}
