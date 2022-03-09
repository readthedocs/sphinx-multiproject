Configuration
=============

You can set the following options in your ``conf.py`` file.

.. confval:: multiproject_projects

   A dictionary defining the projects that will share the configuration.
   You must define at least one project.

   Example:

   .. code-block:: python

      multiproject_projects = {
         "dev": {},
         "user": {},
      }

   Each project can have the following options:

   .. confval:: path

      By default it's the same as the name of the project.
      It can be a relative (to the conf.py file) or an absolute path.

      Example:

      .. code-block:: python

         multiproject_projects = {
            "dev": {
               "path": "path/to/your/project/"
            },
         }

   .. confval:: config

      A dictionary of options specific to this project.
      Useful if you don't want to have a specific ``conf.py`` file
      for each project.

      .. warning::

         There are some options that can't be defined here,
         see :ref:`limitations:pre-init options`.

      Example:

      .. code-block:: python

         multiproject_projects = {
            "dev": {
               "config": {
                     "project": "My project",
               },
            },
         }

   .. confval:: use_config_file

      If `True` the config from ``{path}/conf.py`` would be included for this project.
      Defaults to `True`.

      The values from this file will have precedence over :confval:`config`.

      .. warning::

         There are some options that can't be defined on this file,
         see :ref:`limitations:pre-init options`.

      Example:

      .. code-block:: python

         multiproject_projects = {
            "dev": {
               "use_config_file": True,
            },
         }

.. confval:: multiproject_env_var

   The name of the environment variable to read the current project from.
   Defaults to ``PROJECT``.

   Example:

   .. code-block:: python

      multiproject_env_var = "SPHINX_PROJECT"
