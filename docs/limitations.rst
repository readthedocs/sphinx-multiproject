Limitations
===========

Pre-init options
----------------

Some options are read by Sphinx before any extension is set up,
so changing their values after that won't have the same effect.
These options are:

- :confval:`sphinx:extensions`
- :confval:`sphinx:needs_sphinx`
- :confval:`sphinx:suppress_warnings`
- :confval:`sphinx:language`
- :confval:`sphinx:locale_dirs`

They should be defined outside the :confval:`multiproject_projects` option,
but you can still change these per-project,
see :ref:`advanced-usage:manually changing settings based on the current project`.

app.confdir vs app.srcdir
-------------------------

The value of :py:attr:`app.confdir <sphinx:sphinx.application.Sphinx.confdir>`
will always be the path of the shared ``conf.py`` file,
some extensions/themes may assume that this is the same as
:py:attr:`app.srcdir <sphinx:sphinx.application.Sphinx.srcdir>`,
which can result in some unexpected problems.

The extension/theme shouldn't assume that the configuration directory
is the same as the source directory.

Read the Docs configuration file
--------------------------------

Read the Docs doesn't support having more than one
`configuration file`_ in your repository.

This is a problem if your projects require some specific and incompatible
settings, like a different python version, different requirements,
or different search settings.

.. _configuration file: https://docs.readthedocs.io/en/stable/config-file/v2.html
