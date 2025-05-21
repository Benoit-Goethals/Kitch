.. raw:: html

    <style>
        .row {clear: both}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 0px;
                padding-right: 0px;
                float: left;
            }

            .column3  {
                width: 33.3%;
            }

            .column2  {
                width: 50%;
            }

            .column1  {
                width: 100%;
            }
        }
    </style>

#################
Your Python Tools
#################

.. image:: _static/images/arcelormittal.jpg
    :alt: ArcelorMittal logo
    :scale: 10%
    :align: right

Sphinx-doc (or Sphinx for short) makes it easy to create documentation. This manual explains how you can
create and maintain such a documentation for your project.

On the homepage of the documentation of your Python tools, you will typically
put some welcome word like this. Explain what the purpose is and who to contact
in case of questions. You can change the image also.

.. rst-class:: clearfix row

.. rst-class:: column column2

:ref:`tutorial`
***************
Here you will learn how to create your own documentation.


.. rst-class:: column column2

:ref:`how_to`
*************
Here you can put some tips and tricks.


.. rst-class:: clearfix row
.. rst-class:: column column2

:ref:`reference`
********************
The Reference should give the detailed info for each of your functions.

.. rst-class:: column column2

:ref:`background_info`
**********************
Here we give some info about the history of the package.


.. rst-class:: clearfix row


Contact
*******

For any questions or remarks on this tutorial, contact:

- yves.vindevogel.external@arcelormittal.com
- luc.vandeputte@arcelormittal.com


.. warning::

    This tutorial is far from complete. It's only a starting point for your own
    documentation. If you have suggestions, remarks, spotted errors, please
    feel free to contact us. Any help to improve this tutorial is welcome.


.. note::

    Currently, the tutorial shows you how to make this kind of documentation.
    Once you know enough about this, you can replace this with your own info.

.. toctree::
    :hidden:
    :numbered:
    :maxdepth: 3

    tutorial/index.rst
    how_to/index.rst
    reference/index.rst
    background_info/index.rst
