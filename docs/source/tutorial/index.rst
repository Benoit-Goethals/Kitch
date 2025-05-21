********
Tutorial
********

This tutorial teaches you how to create this style of documentation step-by-step.

.. important::

    This part uses a "table of contents tree", known as a toctree, within
    another toctree. This is because the split of the html pages is done on the
    level of the lowest toctree.

    Each entry in a toctree, creates a new html page.  This means it will start at
    the top of the browser and it will have the previous and next buttons.  In general,
    readers prefer to read shorter pages.

    This is different to including pages in other pages.  These included pages will
    become just part of the other page but will not make a new html page.

    *An example follows in this tutorial.*


**Table of Contents:**

.. toctree::
    :maxdepth: 3

    01_getting_started/index.rst
    02_restructured_text.rst
    03_sphinx.rst
    04_python_documentation.rst
    05_python_project_structure.rst
    06_building_your_documentation.rst
    07_setup_conf_py.rst
    08_exercise.rst


.. note::

    If you don't want this table of contents, add the :hidden: directive to the toctree:

    .. code::

        . toctree::
            :hidden:
            :maxdepth: 3

    On the other hand, it's very handy on the first page. You have an overview of
    the full content and you can jump immediately to the correct information.

.. note::

    The files in the toctree have a prefix number.  This is not needed and you can work without them.  The prefix number helps to easily know the order of the different parts of your content.  However, when you want to insert a part, you need some re-numbering.

    .. code::

        . toctree::
            :maxdepth: 3

        01_getting_started/index.rst
        02_restructured_text.rst
        03_sphinx.rst
        04_python_documentation.rst
        05_python_project_structure.rst
        06_building_your_documentation.rst
        07_setup_conf_py.rst
        08_exercise.rst
    
