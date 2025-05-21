Building your documentation
***************************


From the docs directory, you can now run the batch files to build your documentation:

- **clean.bat**: removes the current directory. This is sometimes needed if
  there is a big structural change in your documentation.
- **build_html.bat**: builds the documentation. The generated documentation is
  under docs/build.
- **view_html.bat**: opens the browser to show your documentation.

.. code:: batch

    (am2210) D:\Development\dept-tools\docs\build\html>dir

     Directory of D:\Development\dept-tools\docs\build\html

    07/02/2024  11:13    <DIR>          .
    07/02/2024  11:13    <DIR>          ..
    07/02/2024  11:13               234 .buildinfo
    07/02/2024  11:13             3.380 genindex.html
    07/02/2024  11:13             4.306 index.html
    07/02/2024  11:13               273 objects.inv
    07/02/2024  11:13             3.794 search.html
    07/02/2024  11:13               686 searchindex.js
    07/02/2024  11:13    <DIR>          _sources
    07/02/2024  11:13    <DIR>          _static
                   6 File(s)         12.673 bytes
                   4 Dir(s)  237.969.199.104 bytes free

You can publish the "html" directory on your intranet for example. You don't
need to publish the "doctrees" directory under "build", it's for sphinx-doc
only.
