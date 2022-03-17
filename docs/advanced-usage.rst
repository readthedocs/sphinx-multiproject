Advanced usage
==============

Using Sphinx's Makefile
-----------------------

Sphinx by default generates a ``Makefile``,
so you can build your documentation with one command:

.. code-block:: console

   $ make html

But when building multiple projects, they will share the same output directory.
Change the ``Makefile`` as follows to set a different build
directory for each project.

.. code-block:: make

   # Put your default project here.
   PROJECT ?= user
   BUILDDIR = _build/$(PROJECT)

Then you can build your documentation with:

.. code-block:: console

   # Will build the user project at _build/user/html/
   $ make html

   # Will build the dev project at _build/dev/html/
   $ PROJECT=dev make html

Manually changing settings based on the current project
-------------------------------------------------------

If the :confval:`config` or :confval:`use_config_file` options aren't enough,
you can change the settings for each project manually.

Using one conf.py file
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # File: docs/conf.py

   from multiproject.utils import get_project

   extensions = [
      "multiproject",
   ]

   multiproject_projects = {
      "user": {},
      "dev": {},
   }

   current_project = get_project(multiproject_projects)

   locale_dirs = [f"{current_project}/locale/"]

   if current_project == "user":
       language = "en"
       extensions += ["custom.extension"]
       project = "User Documentation"
   elif current_project == "dev":
       language = "es"
       project = "Development documentation"

Using multiple conf.py files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # File: docs/conf.py

   extensions = [
      "multiproject",
   ]

   multiproject_projects = {
      # Set `use_config_file` to false
      # to avoid including the files twice.
      "user": {
          "use_config_file": False,
      },
      "dev": {
          "use_config_file": False,
      },
   }

   current_project  = get_project(multiproject_projects)

   # Set all values directly
   # -----------------------

   if current_project == 'user':
      # File: docs/user/conf.py
      from user.conf import *
   elif current_project == 'dev':
      # File: docs/dev/conf.py
      from dev.conf import *

   # Set value by value
   # ------------------

   if current_project == 'user':
      # File: docs/user/conf.py
      import user.conf as config
   elif current_project == 'dev':
      # File: docs/dev/conf.py
      import dev.conf as config

   # Replace the original values.
   project = config.project
   version = config.version
   language = config.language

   # Extending the original value.
   extensions += config.extensions

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
