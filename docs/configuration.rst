Configuration
=============

You can set the following options in your ``conf.py`` file.

.. confval:: multiproject_projects

   A dictionary defining the projects that will share the configuration.
   You must define at least one project, by default the options from each
   project's ``conf.py`` file would be used.

   Example:

   .. code-block:: python

      multiproject_projects = {
         "dev": {},
         "user": {},
      }

   Each project can have the following options:

   .. confval:: path

      Path to the nested project's ``conf.py`` file.
      By default, the key name used in ``multiproject_projects`` is also the directory name for the nested project's ``conf.py`` file.
      This can be a relative path (to the main ``conf.py`` file) or an absolute path.

      Example:

      .. code-block:: python

         multiproject_projects = {
            "dev": {
               "path": "path/to/your/project/"
            },
         }

   .. confval:: config

      A dictionary of options specific to this project.
      This is useful if you don't want to have a specific ``conf.py`` file
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

      If ``True``, the configuration values from ``{path}/conf.py``
      would be automatically imported when building this project.
      Defaults to ``True``.

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
