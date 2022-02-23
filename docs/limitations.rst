Limitations
===========

Pre-init options
----------------

Some options are read by Sphinx before any extension is set up,
so changing their values after that won't have the same effect.
These options are:

- :confval:`sphinx:needs_sphinx`
- :confval:`sphinx:suppress_warnings`
- :confval:`sphinx:language`
- :confval:`sphinx:locale_dirs`

They should be defined outside the :confval:`sharedconf_docsets` option,
but you can still change these per-project, see :ref:`advanced-usage:changing settings depending on the current docset`.

app.confdir vs app.srcdir
-------------------------

The value of :py:attr:`app.confdir <sphinx:sphinx.application.Sphinx.confdir>`
will always be the path of the shared ``conf.py`` file,
some extensions/themes may assume that this is the same as
:py:attr:`app.srcdir <sphinx:sphinx.application.Sphinx.srcdir>`,
which can result in some unexpected problems.

The extension/theme shouldn't assume that the configuration directory
is the same as the source directory.
