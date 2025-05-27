Sphinx
******

What is Sphinx ?
================

.. image:: /_static/images/tutorial_002.png
    :scale: 50%

From https://www.sphinx-doc.org

**Sphinx makes it easy to create intelligent and beautiful documentation.**

Here are some of Sphinx's major features:

    - **Output formats**: HTML (including Windows HTML Help), LaTeX (for
      printable PDF versions), ePub, Texinfo, manual pages, plain text
    - **Extensive cross-references**: semantic markup and automatic links for
      functions, classes, citations, glossary terms and similar pieces of
      information
    - **Hierarchical structure**: easy definition of a document tree, with
      automatic links to siblings, parents and children
    - **Automatic indices**: general index as well as a language-specific
      module indices
    - **Code handling**: automatic highlighting using the Pygments highlighter
    - **Extensions**: automatic testing of code snippets, inclusion of
      docstrings from Python modules (API docs) via built-in extensions, and
      much more functionality via third-party extensions.
    - **Themes**: modify the look and feel of outputs via creating themes, and
      reuse many third-party themes.
    - **Contributed extensions**: dozens of extensions contributed by users;
      most of them installable from PyPI.

**Sphinx uses the reStructuredText markup language by default**, and can read
MyST markdown via third-party extensions. Both of these are powerful and
straightforward to use, and have functionality for complex documentation and
publishing workflows. They both build upon Docutils to parse and write
documents.


Why **we** use Sphinx
=====================

We use Sphinx because:

- it automates a big part of our documentation work because it is made to
  document Python.
- it is *coding* the documentation, which means we can easily write small parts
  of documentation specifically for what we developed. We can document
  simultaneously with multiple developers.
- it allows us to review the documentation, in a similar way as we review the
  code.
- it allows us to version the documentation as we store the documentation in
  GitHub / Azure DevOps. Who did what when, basically.
- it allows us to generate the final documentation without having to care much
  about the layout. Once generated, we can easily publish the documentation
  online so it becomes available to everybody.

