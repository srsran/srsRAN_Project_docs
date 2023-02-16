.. _commit_formatting: 

Commit Formatting
#################

When committing code to the srsRAN Project codebase it is important that commit messages are clear and succinct. This means having clear guidelines for 
how commits should be structured, both in the title and body of the commit messages. 

The preferred commit message style is as follows:

.. code-block:: console

    component: brief change description 

Here, component refers to the section of the codebase being modified by the commit. Some examples of this could be: 

    - ``mac_test``, ``equalizer`` - changes are limited to a specific function/class
    - ``phy``, ``mac``, ``rlc``, etc - multiple changes across a specific layer
    - ``cmake`` - changes to the cmake file 
    - ``all`` - a commit modifies something across the whole codebase 
    - ``misc`` - a miscellaneous change 

Multiple components can be used if a commit touches two or more components. Simply separate the components with a comma.  For example:

.. code-block:: console

    rlc, mac: some commit message 

The brief change description should be just that, *brief*. This means no more than 50 characters, including the component(s). This ensures that the commit message will be displayed 
properly with no cuts. If you need to create a commit message with more information, the body of the commit message may be used. To do this, separate the heading from the body 
with a line break in your editor. For example:

.. code-block:: console

    component: brief commit outline less than 50 char

    Body of commit message giving more detail about the commit. This should 
    only be used when further explanation is needed. This can span multiple 
    lines if necessary, but keep it as succinct as possible. 

Note that all words in the subject line are lower case and there is no trailing period. 

To summarize, here are a few brief points to follow when committing to the srsRAN codebase: 

    - Each commit should have a ``component`` and a ``brief outline``
    - Commit subject lines should be limited to 50 characters in total 
    - The body of a commit should be separated by a line break 
    - Keep all text as succinct as possible 
    - No upper case letters or trailing period in subject line

If you would like more information on writing "good" commits, `this guide <https://cbea.ms/git-commit/>`_ is a useful resource. 
 