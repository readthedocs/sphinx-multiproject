Configuration
=============

You can set the following options in your ``conf.py`` file.

.. confval:: multiproject_projects

   A dictionary defining the projects that will share the configuration.
   You must define at least one docset.

   Each docset can have the following options:

   path
     By default it's the same as the name of the docset.
     It can be a relative (to the conf.py file) or an absolute path.

   config
     A dictionary of options specific to this docset.

     .. warning::

        There are some options that can't be defined here,
        see :ref:`limitations:pre-init options`.

   Example:

   .. code-block:: python

      multiproject_env_var = {
         "user": {},
         "dev": {
            "path": "path/to/your/docset/"
            "config": {
                  "project": "My project",
            },
         },
      }

.. confval:: multiproject_env_var

   The name of the environment variable to read the current docset from.
   Defaults to ``DOCSET``.

   Example:

   .. code-block:: python

      multiproject_env_var = "SPHINX_PROJECT"
