# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'housenum-be-r-parser'
copyright = '2019 Onroerend Erfgoed'  # noqa: A001 shadowed builtin
author = 'Onroerend Erfgoed'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]

nitpicky = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'sphinx_rtd_theme'
# the oe theme doesn't look good for API documentation imo.
# import oe_sphinx_theme
# html_theme_path = [oe_sphinx_theme.get_theme_dir()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# -- intersphinx
intersphinx_mapping = {'py': ('https://docs.python.org/3.6', None)}

# -- autodoc
autoclass_content = 'both'  # This adds __init__ documentation.

# -- rtd theme
html_theme_options = {
    'navigation_depth': 6,
}
