Quickstart
==========

Installation
------------

Install the extension:

.. code-block:: console

   $ pip install sphinx-multiproject

Usage
-----

You can structure your project like this:

.. code-block::

   docs
   ├── conf.py
   ├── dev
   │   ├── conf.py
   │   └── index.rst
   └── user
       ├── conf.py
       └── index.rst

Where ``docs/conf.py`` would be your shared configuration file,
and ``docs/dev/`` and ``docs/user/`` would be your projects
using their specific configuration file.

.. code-block:: python

   # File: docs/conf.py

   extensions = [
      "multiproject",
      # Your other extensions.
      "sphinx.ext.intersphinx",
      ...
   ]

   # Define the projects that will share this configuration file.
   multiproject_projects = {
       "user": {},
       "dev": {
           # Set a custom path.
           "path": "dev",
       },
   }

   # Common options.
   html_theme = "sphinx_rtd_theme"

Then build your project as usual.

.. code-block:: console

   # Build the default project (user)
   $ sphinx-build . _build/user/html

Or you can build each project by chaning the ``PROJECT`` environment variable.

.. code-block:: console

   # Build the dev project
   $ PROJECT=dev sphinx-build . _build/dev/html

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
called ``PROJECT`` with the proper value of the project you want to build.

.. _.readthedocs.yaml: https://docs.readthedocs.io/page/config-file/v2.html
.. _environment variable: https://docs.readthedocs.io/page/environment-variables.html
