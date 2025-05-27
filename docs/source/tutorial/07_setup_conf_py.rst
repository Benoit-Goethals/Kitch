Setting Up the conf.py File
***************************

Default file
============

At the moment of writing this tutorial, the conf.py file in the root directory
of this repository has the following content.

In this chapter, this content is explained line by line, but only for the
things you should change. This is standard Python, so feel free to adapt it.
But make sure it works with sphinx-doc.

.. code:: python

    # Configuration file for the Sphinx documentation builder.
    #
    # For the full list of built-in configuration values, see the documentation:
    # https://www.sphinx-doc.org/en/master/usage/configuration.html

    # -- Project information -----------------------------------------------------
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

    from datetime import datetime

    project = 'Project'  # Rename this to your own project name
    author = 'ArcelorMittal'  # This will appear in the copyright
    release = '0.0.1'

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
        'style_nav_header_background': '#FF3801',

        # Toc options
        'collapse_navigation': True,
        'sticky_navigation': True,
        'navigation_depth': 2,  # This determines the number of levels in the left content menu
        'includehidden': True,
        'titles_only': False
    }

Possible updates
================

.. code:: python

    project = 'Project'  # Rename this to your own project name

The above line determines the name of your project. Most likely this will
become the name of your Python tools, like "depttools". Rename this to what you
want and recompile the site using the build_html.bat file.

.. image:: /_static/images/tutorial_001.png

.. code:: python

    author = 'ArcelorMittal'  # This will appear in the copyright

The author appears at the bottom of your documentation site. Leave it as it is,
but maybe one day this could change after a giant merger in the steel industry.

.. code:: python

    release = '0.0.1'

This is the version of your tools. Update it according to the evolution of your
tools.

.. code:: python

    project_start = 2023

This is when your project, your tools, start.  It is used in the copyright:

- If the year is still 2023 in this case, the copyright is "Copyright 2023 - ArcelorMittal"
- If the year is no longer 2023, but 2024 for example, the copyright is "Copyright 2023-2024 - ArcelorMittal"

.. code:: python

    # html_logo = '_static/images/sphinx_2.png'  # Set this in comment to remove the logo

You can uncomment this line and put your own logo in the top corner of the left menu

.. code:: python

    html_show_sourcelink = True

This shows or hides the "View page source" at the top right corner of each page.
This can be handy to see how somebody has written a certain page.

.. code:: python

    'navigation_depth': 3,  # This determines the number of levels in the left content menu

This line determines how many levels of submenu's there are in the left menu.
Set this either to 2 or 3.

.. caution::

    You can of course change all the parameters in the conf.py file, but that
    should normally not be necessary. The above ones may be useful, but leave
    the others as they are, unless you know what you are changing and why.
