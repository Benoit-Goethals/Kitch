ReStructured Text (rst)
***********************

What is RST ?
=============

.. image:: /_static/images/tutorial_003.png

From https://docutils.sourceforge.io/rst.html:

**ReStructuredText is an easy-to-read, what-you-see-is-what-you-get plaintext
markup syntax and parser system. It is useful for in-line program documentation
(such as Python docstrings), for quickly creating simple web pages, and for
standalone documents.** reStructuredText is designed for extensibility for
specific application domains. The reStructuredText parser is a component of
Docutils. reStructuredText is a revision and reinterpretation of the
StructuredText and Setext lightweight markup systems.

**The primary goal of reStructuredText is to define and implement a markup
syntax for use in Python docstrings and other documentation domains, that is
readable and simple, yet powerful enough for non-trivial use.**
The intended purpose of the markup is the conversion of reStructuredText
documents into useful structured data formats.


Some principles
===============

RST, like Markdown, is a markup language that let's you concentrate on the
content and not on the looks of the document. Whereas with some other tools
like Microsoft Word, you spend a lot of time on the look of the document,
aligning bullets, setting numbering, ... in RST you just type text and in
combination with Sphinx you will get a correct final layout.

RST "removes" some nasty things from your typing. For instance, if you leave
one space or 2 spaces after the period at the end of the sentence, RST ignores
this and puts one. If you add 1 blank line or 2 blank lines, RST will put 1 in
the final output document. So, focus on writing the content and let RST handle
the output.


Some examples
=============

Paragraphs
----------

You can just start typing your text and this will become a paragraph. As long as you continue on a line, without wrapping to the next line, the paragraph will continue. In your final document, the text will be nicely wrapped to the next line(s). Like this line.

If you prefer to have smaller lines,
just press enter at the end of the line
and continue typing.
In the final result, you don't see it,
but in my RST, this paragraph was
spread over 6 lines.


To go to a new item, like a bullet list, just leave one blank line. Leaving
more than one line is not a problem. You will not notice. Same with spaces in
the paragraph.

.. code:: restructuredtext

    You can just start typing your text and this will become a paragraph.  As long as you continue on a line, without wrapping to the next line, the paragraph will continue. In your final document, the text will be nicely wrapped to the next line(s). Like this line.

    If you prefer to have smaller lines,
    just press enter at the end of the line
    and continue typing.
    In the final result, you don't see it,
    but in my RST, this paragraph was
    spread over 7 lines.


    To go to a new item, like a bullet list, just leave one blank line.
    Leaving more than one line is not a problem. You will not notice. Same with
    spaces in the paragraph.


Indentation
-----------

RST uses indentation to group things, just as Python does. For example, when
you have a code block, all what is indented is in that code block. As soon as
you leave the indentation, you are out of the block.

.. code:: python

    print("This is within the block, so seen as Python code")

This line is outside the block and is standard text again.


.. code:: restructuredtext

    .. code:: python

        print("This is within the block, so seen as Python code")

    This line is outside the block and is standard text again.


Bold and italic
---------------

**You can easily put a line in bold by adding double asterix in front and at the end of the line.**

*The same can be done with italic, just add one asterix in front and at the end.*

.. code:: restructuredtext

    **You can easily put a line in bold by adding double asterix in front and at the end of the line.**

    *The same can be done with italic, just add one asterix in front and at the end.*


Bullet lists
------------

- You can easily create a bullet list by adding the minus sign (-) in front of your text.
- As long as you continue with the minus signs, the bullet list continues.
- Instead of the minus sign, you can also use the plus sign (+) or the asterix (*).

.. code:: restructuredtext

    - You can easily create a bullet list by adding the minus sign (-) in front of your text.
    - As long as you continue with the minus signs, the bullet list continues.
    - Instead of the minus sign, you can also use the plus sign (+) or the asterix (*).


Enumerated lists
----------------

1. This is not so automatically. You must put the 1. in front of the first item.
2. And 2. in front of the next. Counting is not automatically done.

.. code:: restructuredtext

    1. This is not so automatically. You must put the 1. in front of the first item.
    2. And 2. in front of the next. Counting is not automatically done.

Code
----

.. code:: python

    import arcelormittal as am

    # You can easily put code in your documents, like examples, with color
    # highlighting according to the language

.. code:: batch

    REM It even supports old batch files

    @echo Hello Redmond

.. code:: restructuredtext

    .. code:: python

        import arcelormittal as am

        # You can easily put code in your documents, like examples, with color
        # highlighting according to the language

    .. code:: batch

        REM It even supports old batch files

        @echo Hello Redmond

Images
------

Below is an image at 20% scale

.. image:: /_static/images/sphinx_1.png
   :scale: 20%

.. code:: restructuredtext

    .. image:: /_static/images/sphinx_1.png
       :scale: 20%


Structure in the document
=========================

A structure in the document is created by underlining (and optionally overlining) the titles with a punctuation character, at least as long as the text:

.. code::

    =================
    This is a heading
    =================


Normally, there are no heading levels assigned to certain characters as the structure is determined from the succession of headings. However, this convention is used in `Python Developer’s Guide for documenting <https://devguide.python.org/documentation/markup/#sections>`_ which you may follow:

    - # (hashtag) with overline, for parts
    - \* (asterix) with overline, for chapters
    - = (equal sign) for sections
    - \- (minus sign) for subsections
    - ^ (hat) for sub-subsections
    - " (double quote) for paragraphs


The full list of possibilities
==============================

This tutorial is not a tutorial on RST alone, therefore if you want to learn all the possibilities, please have a look at the following website where you will have a full overview of RST's functionality.

https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html

