# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import datetime
sys.path.insert(0, os.path.abspath('../src'))
project = 'Sphinx-doc'  # Rename this to your own project name
author = 'Kitch'  # This will appear in the copyright
release = '1.0.0'

###
# sidviny - 2023-12-21
# Put the year you started this documentation site in project_start.
# This will automatically set the years in the copyright to the project_start or to project_start-current year
project_start = 2023

if datetime.now().year == project_start:
    copyright = f'{project_start} - {author}'  # noqa
else:
    copyright = f'{project_start}-{datetime.now().year} - {author}'  # noqa
###

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'sphinx.ext.autosectionlabel']

templates_path = ['_templates']
exclude_patterns = ['**/*inc.rst']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_title = f'{project} v{release}'  # Comment this to have the default
# html_logo = '_static/images/sphinx_2.png'  # Set this in comment to remove the logo
html_css_files = ['css/arcelormittal.css']
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True
html_static_path = ['_static']


# The options below are specific to the sphinx_rtd_theme

html_theme_options = {
    # 'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
    # 'analytics_anonymize_ip': False,
    'logo_only': False,  # Setting this to False, will show the home link above the logo
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#F77304',

    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 3,  # This determines the number of levels in the left content menu
    'includehidden': True,
    'titles_only': False
}
