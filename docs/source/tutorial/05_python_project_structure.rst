Python Project Structure
************************

Directory structure
===================


When you start to develop your own Python tools project, we recommend the
following structure:

.. code::

    <root_directory>  -> something like your_department-tools
        |
        ├── <your_department_tools>
        ├── docs
        ├── resources
        ├── tests
        └── <any_other_directory>

You should put this in a git repository in Azure DevOps. Contact us for help if
needed.


- **<your_department_tools>**: here goes the actual code of your Python tools
  package. The contents of this folder will eventually be copied to:
  <Sharepoint>\\ArcelorMittal\\AMPythonBelgium - Tools\\packages\\<your_department_tools>

.. image:: /_static/images/tutorial_004.png

.. important::

    You should ask Raphael Ottevaere to set up a pipeline in Azure DevOps to copy your code to this location.  We could include it in your tasks, but it's far from evident if you have not done it before.  For Raf, it takes 5 minutes.

.. important::

    We have already put the path above until "packages" in your PYTHONPATH.  This means that everybody who uses Python, automatically will have access to your tools.

.. image:: /_static/images/tutorial_005.png

**Other directories**

- **docs**: this is where the documentation will go. So the cloned repository goes here.
- **resources**: any file you need for the project, like Word files, images, ...
- **tests**: here is where your tests go.  Normally, for all code, there should be an automated test.


Cloning the repository
======================

Project structure
-----------------

Assume we make a new package, called **dept_tools**. We first make the base
directories. We do this in File Explorer or in a Command Prompt window. If you
are more familiar with PowerShell or WSL, feel free to do the same commands in
those shell environments. In  the example below we created the **dept-tools**
directory in D:\Development, but you could also put it in
**%UserProfile%\Documents\Python**

.. code:: batch

    mkdir dept-tools
    cd dept-tools
    mkdir dept_tools
    mkdir tests
    mkdir resources

.. code:: batch

    (am2311) D:\Development\dept-tools>dir

     Directory of D:\Development\dept-tools

    07/02/2024  10:31    <DIR>          .
    07/02/2024  10:31    <DIR>          ..
    07/02/2024  10:21    <DIR>          resources
    07/02/2024  10:21    <DIR>          tests
    07/02/2024  10:21    <DIR>          dept_tools
                   0 File(s)              0 bytes
                   5 Dir(s)  237.974.765.568 bytes free


Local Git repository
--------------------

It's best to put this directory in a Git repo and put it in AzureDevops.
The following commands are best executed in **Git Bash**:

.. code:: batch

    git init
    git branch -m master
    git checkout -b master

.. code:: batch

    (am2311) D:\Development\dept-tools>git init
    hint: Using 'master' as the name for the initial branch. This default branch name
    hint: is subject to change. To configure the initial branch name to use in all
    hint: of your new repositories, which will suppress this warning, call:
    hint:
    hint:   git config --global init.defaultBranch <name>
    hint:
    hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
    hint: 'development'. The just-created branch can be renamed via this command:
    hint:
    hint:   git branch -m <name>
    Initialized empty Git repository in D:/Development/dept-tools/.git/

    (am2311) D:\Development\dept-tools>git branch -m master

    (am2311) D:\Development\dept-tools>git checkout -b master
    Switched to a new branch 'master'


Azure DevOps Git repository
---------------------------

This part we have to do in a browser. Connect to
`Azure DevOps <http://wftfsprod.sidmar.be:8080/tfs/IAM/IAM-SYMO-PD/_git/py-dex>`_
and choose "Manage repositories" from the menu.

.. image:: /_static/images/tutorial_008.png

When you have all the repositories, select the "Create" button.

.. image:: /_static/images/tutorial_009.png

Give your repository a name and set the other options according to this
example, and press "Create"

.. image:: /_static/images/tutorial_010.png

If you now select the newly created repository, you will find it empty.
We have to link the local repository to the remote one. To do so, copy the code
proposed in Azure DevOps and execute it in the shell.

.. image:: /_static/images/tutorial_011.png

.. code:: batch

    (am2311) D:\Development\dept-tools>git remote add origin http://wftfsprod.sidmar.be:8080/tfs/IAM/IAM-SYMO-PD/_git/dept-tools

    (am2311) D:\Development\dept-tools>git push -u origin --all
    No refs in common and none specified; doing nothing.
    Perhaps you should specify a branch.
    Everything up-to-date


The docs directory
------------------

The next directory we need, is the docs directory. This is where we will clone
this repository to get a starting point.

.. image:: /_static/images/tutorial_006.png

.. image:: /_static/images/tutorial_007.png

.. code:: batch

    git clone http://wftfsprod.sidmar.be:8080/tfs/IAM/IAM-SYMO-PD/_git/sphinx-doc

.. code:: batch

    (am2210) D:\Development\dept-tools>git clone http://wftfsprod.sidmar.be:8080/tfs/IAM/IAM-SYMO-PD/_git/sphinx-doc
    Cloning into 'sphinx-doc'...
    remote: Azure Repos
    remote: Found 47 objects to send. (3 ms)
    Unpacking objects: 100% (47/47), 111.23 KiB | 1.41 MiB/s, done.

    (am2311) D:\Development\dept-tools>dir

     Directory of D:\Development\dept-tools

    07/02/2024  10:35    <DIR>          .
    07/02/2024  10:35    <DIR>          ..
    07/02/2024  10:21    <DIR>          resources
    07/02/2024  10:36    <DIR>          sphinx-doc
    07/02/2024  10:21    <DIR>          tests
    07/02/2024  10:21    <DIR>          dept_tools
                   0 File(s)              0 bytes
                   6 Dir(s)  237.974.429.696 bytes free

Note that the newly created directory is not called docs, but sphinx-doc.
Rename it to docs

.. code:: batch

    rename sphinx-doc docs

.. code:: batch

    (am2311) D:\Development\dept-tools>dir

     Directory of D:\Development\dept-tools

    07/02/2024  10:58    <DIR>          .
    07/02/2024  10:58    <DIR>          ..
    07/02/2024  10:57    <DIR>          docs
    07/02/2024  10:21    <DIR>          resources
    07/02/2024  10:21    <DIR>          tests
    07/02/2024  10:21    <DIR>          dept_tools
                   0 File(s)              0 bytes
                   6 Dir(s)  237.973.680.128 bytes free


Note that there is still a link with the repository for docs. We don't want
that as this documentation becomes an integral part of your project. By
removing the hidden .git directory in the docs directory, we remove the link.
The .gitignore file is not needed either, so it can be removed.

.. code:: batch

    (am2311) D:\Development\dept-tools\docs>dir /a

     Directory of D:\Development\dept-tools\docs

    07/02/2024  10:57    <DIR>          .
    07/02/2024  10:57    <DIR>          ..
    07/02/2024  10:57    <DIR>          .git
    07/02/2024  10:57               160 .gitignore
    07/02/2024  10:57                11 build_html.bat
    07/02/2024  10:57                19 clean.bat
    07/02/2024  10:57               804 make.bat
    07/02/2024  10:57               658 Makefile
    07/02/2024  10:57               307 README.md
    07/02/2024  10:57    <DIR>          source
    07/02/2024  10:57                89 view_html.bat
                   7 File(s)          2.048 bytes
                   4 Dir(s)  237.973.680.128 bytes free

.. code:: batch

    rmdir /S .git
    del .gitignore

.. code:: batch

    (am2311) D:\Development\dept-tools\docs>rmdir /S .git
    .git, Are you sure (Y/N)? y

.. code:: batch

    (am2311) D:\Development\dept-tools\docs>dir /a

     Directory of D:\Development\dept-tools\docs

    07/02/2024  11:05    <DIR>          .
    07/02/2024  11:05    <DIR>          ..
    07/02/2024  10:57                11 build_html.bat
    07/02/2024  10:57                19 clean.bat
    07/02/2024  10:57               804 make.bat
    07/02/2024  10:57               658 Makefile
    07/02/2024  10:57               307 README.md
    07/02/2024  10:57    <DIR>          source
    07/02/2024  10:57                89 view_html.bat
                   6 File(s)          1.888 bytes
                   3 Dir(s)  237.973.860.352 bytes free

It is now a good time to commit this. Note that you will have more files than
in the example below. There are more files in this repository now.

.. code:: batch

    (am2311) D:\Development\dept-tools>git status
    On branch master

    No commits yet

    Untracked files:
      (use "git add <file>..." to include in what will be committed)
            docs/

    nothing added to commit but untracked files present (use "git add" to track)

    (am2311) D:\Development\dept-tools>git add .

    (am2311) D:\Development\dept-tools>git commit -m "Documentation"
    [master (root-commit) b7e2632] Documentation
     14 files changed, 175 insertions(+)
     create mode 100644 docs/Makefile
     create mode 100644 docs/README.md
     create mode 100644 docs/build_html.bat
     create mode 100644 docs/clean.bat
     create mode 100644 docs/make.bat
     create mode 100644 docs/source/_static/css/arcelormittal.css
     create mode 100644 docs/source/_static/images/arcelormittal.jpg
     create mode 100644 docs/source/_static/images/sphinx_1.png
     create mode 100644 docs/source/_static/images/sphinx_2.png
     create mode 100644 docs/source/_static/images/sphinx_3.png
     create mode 100644 docs/source/_static/images/sphinx_4.png
     create mode 100644 docs/source/conf.py
     create mode 100644 docs/source/index.rst
     create mode 100644 docs/view_html.bat
