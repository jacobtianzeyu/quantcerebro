# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys
import pathlib
import toml

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

__version__ = None
__author__ = None
__copyright__ = None
__project__ = None

pyproject_config = toml.load('../../pyproject.toml')

release = pyproject_config['tool']['poetry']['version']
author = "; ".join(pyproject_config['tool']['poetry']['authors'])
copyright = "Copyright 2022, The QuantCerebro Project"
project = pyproject_config['tool']['poetry']['name']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = False
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    # formats
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon', # to accept markdown and numpy type docstring (as default parsing is rst)
    # doc test
    'sphinx.ext.duration',
    'sphinx.ext.doctest',]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': 'abc.com',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
html_static_path = ['_static']

# -- Options for Autodoc output ---------------------------------------------
autodoc_mock_imports = []
autoclass_content = 'class'
autodoc_member_order = "bysource"
autodoc_default_flags = [
    'members',
    'undoc-members'
    ]
