Quickstart
==========

Installation
------------

Install the extension:

.. code-block:: console

   $ pip install sphinx-sharedconf

Usage
-----

You can structure your project like this:

.. code-block::

   docs
   ├── conf.py
   ├── dev
   │   └── index.rst
   └── user
       └── index.rst

Where ``docs/conf.py`` would be your shared configuration file,
and ``docs/dev/`` and ``docs/user/`` would be your projects using that
configuration file.

.. code-block:: python

   # File: docs/conf.py

   extensions = [
      "sharedconf.extension",
      # Your other extensions.
      "sphinx.ext.intersphinx",
      ...
   ]

   # Define the projects that will share this configuration file.
   sharedconf_docsets = {
       "user": {
           "config": {
               # Specific options for this docset.
               "project": "User documentation",
           },
       },
       "dev": {
           # Set a custom path.
           "path": "dev",
           "config": {
               # Specific options for this docset.
               "project": "Developer documentation",
           },
       },
   }

   # Common options
   html_theme = "sphinx_rtd_theme"

Then build your project as usual.

.. code-block:: console

   # Build the default docset (user)
   $ sphinx-build . _build/user/html

Or you can build each docset by chaning the ``DOCSET`` environment variable.

.. code-block:: console

   # Build the dev docset
   $ DOCSET=dev sphinx-build . _build/dev/html

Importing your projects on Read the Docs
----------------------------------------

Define your `.readthedocs.yaml`_ file as usual:

.. code-block:: yaml

   version: 2

   build:
   os: ubuntu-20.04
   tools:
      python: "3.9"
   sphinx:
      # Path to the shared conf.py file.
      configuration: docs/conf.py

And on each project create an `environment variable`_
called ``DOCSET`` with the proper value of the docset you want to build.

.. _.readthedocs.yaml: https://docs.readthedocs.io/page/config-file/v2.html
.. _environment variable: https://docs.readthedocs.io/page/environment-variables.html
