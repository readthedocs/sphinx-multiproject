Advanced usage
==============

Using Sphinx's Makefile
-----------------------

Sphinx by default generates a ``Makefile``,
so you can build your documentation with one command:

.. code-block:: console

   $ make html

But when building multiple docsets, they will share the same output directory.
Change the ``Makefile`` as follows to set a different build
directory for each docset.

.. code-block:: make

   # Put your default docset here.
   DOCSET ?= user
   BUILDDIR = _build/$(DOCSET)

Then you can build your documentation with:


.. code-block:: console

   # Will build the user docset at _build/user/html/
   $ make html

   # Will build the dev docset at _build/dev/html/
   $ DOCSET=dev make html

Changing settings depending on the current docset
-------------------------------------------------

If the ``config`` option of the :confval:`sharedconf_docsets` option isn't enough,
you can check for the current docset in your ``conf.py`` file as follows:

.. code-block:: python

   # File: conf.py

   from sharedconf.utils import get_docset

   extensions = [
      "sharedconf.extension",
   ]

   sharedconf_docsets = {
      "user": {},
      "dev": {},
   }

   docset = get_docset(sharedconf_docsets)

   locale_dirs = [f"{docset}/locale/"]

   if docset == "user":
       language = "en"
       extensions += ["custom.extension"]
   elif docset == "dev":
       language = "es"

Sharing a conf.py file without using an extension
-------------------------------------------------

If you aren't restricted to share the same location of the ``conf.py`` file
for all your projects, you can just use an ``import`` statement on each project.
For example, in the following structure:

.. code-block::

   docs
   ├── conf.py
   ├── dev
   │   ├── conf.py
   │   └── index.rst
   └── user
      ├── conf.py
      └── index.rst

The ``docs/conf.py`` file has the shared configuration,
and each ``docs/dev/conf.py``, ``docs/user/conf.py`` files
have specific configuration for that project:

.. code-block:: python

   # File: docs/conf.py
   # Common options for all projects.

   language = "en"
   extensions = ["sphinx.ext.intersphinx"]

.. code-block:: python

   # File: docs/dev/conf.py
   # Options specific to this project.

   from ..conf import *

   extensions = extensions + [
       "custom.extension",
   ]

   project = "Developer documentation"
