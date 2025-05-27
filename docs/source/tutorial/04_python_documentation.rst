Python Documentation
********************

Using docstrings
================

The base of good Python documentation are proper docstrings.

.. |documentation_link| raw:: html

    <a href="https://intranetamb.sidmar.be/ampython/documentation/docs/how_to/write_documentation.html"
        target="_blank">https://intranetamb.sidmar.be/ampython/documentation/docs/how_to/write_documentation.html</a>

A full chapter has already been provided on the Help pages of the AMPython documentation:
|documentation_link|


Usage in the documentation
==========================

You can use these docstrings to automatically write your documentation.
When you are building your documentation using the latest AMPython environment
(am2210, am2311, ...), you can do an import of your tools. You can then easily
take the docstring of a function you wrote using the following code.

For example, the code:

.. code:: python

    def sign(extra_text: str = ''):
    """Print date, time, username and text as a string.

    Use this after importing the arcelormittal package in order to show
    when the code was executed, by which user it was executed and who can be
    contacted in case of questions.

    YYYY-mm-DD HH:MM:SS - username - text

    Example::

        am.sign('author: luc.vandeputte@arcelormittal.com')

    """
    signed_text = f'Last executed on {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} by {os.getlogin()}'
    if extra_text == '':
        return signed_text
    else:
        return f"{signed_text} - {extra_text}"

You can inject this docstring into the documentation with:

.. code::

    .. autofunction:: arcelormittal.sign

Automatically, the docstring is then included as shown below.

.. autofunction:: arcelormittal.sign

.. caution::

    *In general you do:*

    .. code:: python

        import arcelormittal as am

    *and then call the functions with:*

    .. code:: python

        am.sign()

    *For the documentation, you cannot use the "am" abbreviation but you must use the full "arcelormittal" module name.*
