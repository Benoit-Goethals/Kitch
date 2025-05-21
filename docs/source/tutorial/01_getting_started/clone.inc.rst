Clone the repo
==============

This documentation on how to build a documentation site with Sphinx is
stored in a Git repository on AzureDevops. The location is:
http://wftfsprod.sidmar.be:8080/tfs/IAM/IAM-SYMO-PD/_git/sphinx-doc

If you want to start your own documentation site, you should clone this repo
locally. Once cloned, detach it and copy it to your project as explained
further on.

.. warning::

    Do not push to the original repository. You must detach the repo by
    removing the .git directory. Then it becomes an integral part of your
    documents.

You need to choose a branch strategy for your code. We suggest to use branch
strategy based on the standard GitHub Flow branching model:

.. image:: /_static/images/tutorial_013.png

- **master**: the final documentation. See this as the production code in
  a standard coding project.
- **feature/xyz**: use feature branches when you are updating the documentation.
  Each time you have finished a part, do a commit in Git. Finally, when you as
  a writer consider your work to be finished, do a pull request of your feature
  branch into the master branch.

.. important::

    As this becomes part of your project, just use the same branching strategy
    as your project.

.. note::

    The above branching strategy is fully compatible with Azure DevOps.
