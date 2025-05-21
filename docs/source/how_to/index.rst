.. _how_to:

******
How-to
******

| This chapter provides some code examples on how to write things in reStructuredText.
| For a complete list of possibilities, visit:
| https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html


.. note::

    If you have nice examples, let us know and we will include them here.


Write comments
==============

You can easily add comments in your files, for instance at the top to include
the author and the date you wrote this.


.. code:: restructuredtext

    .. version: 1.0.0
    .. author: yves.vindevogel.external@arcelormittal.com
    .. date: 2024-02-12


Show Python code
================

You can add code, with syntax highlighting, to your documentation using the code directive.


.. code:: restructuredtext

    .. code:: python

        import arcelormittal as am

        print(am.user())

There are several coding languages that are supported.  In this document I used:

- python
- batch
- restructuredtext


Include docstrings
==================

To include a docstring of a function, you can write a reference like this:

.. code:: restructuredtext

    .. autofunction:: arcelormittal.sign

The result is:

.. autofunction:: arcelormittal.sign
    :noindex:


New line without whitespace
===========================

You can force a new line without a whitespace (blank line) by putting
the pipe character (|) in front of the lines.

| For example:
| This line is stuck to the "For example":

.. code:: restructuredtext

    | For example:
    | This line is stuck to the "For example":
