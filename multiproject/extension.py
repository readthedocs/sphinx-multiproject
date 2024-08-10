from pathlib import Path

from sphinx.config import CONFIG_FILENAME, eval_config_file
from sphinx.util import logging

from .utils import get_project

log = logging.getLogger(__name__)

__version__ = "1.0.0rc1"


def _get_project_from_config(config):
    project = get_project(
        config.multiproject_projects,
        config.multiproject_env_var,
    )
    return project, config.multiproject_projects[project]


def _override_srdir(app, config):
    """
    Override app.srcdir with the value from the current project.

    If the project doesn't have a path,
    the name of the project is used as the path.

    Values can be absolute or relative to the original source dir.
    """
    project, options = _get_project_from_config(config)
    log.info("Using project: %s", project)

    original_srcdir = Path(app.srcdir)
    new_srcdir = Path(options.get("path", project))
    if not new_srcdir.is_absolute():
        new_srcdir = original_srcdir / new_srcdir
    # app.srcdir is a Path object and not 'str' in newer versions of Sphinx
    # app.srcdir = str(new_srcdir.resolve())
    app.srcdir = new_srcdir.resolve()


def _override_config(app, config):
    """Override the config with specific values from the current project."""
    _, options = _get_project_from_config(config)
    project_config = options.get("config", {})
    if options.get("use_config_file", True):
        config_file = Path(app.srcdir) / CONFIG_FILENAME
        if config_file.exists():
            project_config.update(
                eval_config_file(
                    filename=str(config_file),
                    tags=None,
                )
            )
        else:
            log.warning("The %s file doesn't exist.", config_file)

    # Taken from
    # https://github.com/sphinx-doc/sphinx/blob/586de7300a5269de93b4d813408ffdbf10ce2409/sphinx/config.py#L222-L222
    pre_init_options = {
        "extensions",
        "needs_sphinx",
        "suppress_warnings",
        "language",
        "locale_dirs",
    }
    for option, value in project_config.items():
        if option in pre_init_options:
            log.warning(
                "Setting the `%s` option from the extension options won't have the desired effect. "
                "Please see https://sphinx-multiproject.readthedocs.io/page/limitation.html#pre-init-options",
                option,
            )
        config[option] = value


def _config_inited(app, config):
    _override_srdir(app, config)
    _override_config(app, config)


def setup(app):
    app.add_config_value(
        "multiproject_env_var",
        default="PROJECT",
        rebuild="env",
        types=[str],
    )
    app.add_config_value(
        "multiproject_projects",
        default={},
        rebuild="env",
        types=[dict],
    )

    # Priority should be as low as possible, so other extensions that
    # depend on the srcdir or the project config use the new values.
    app.connect(
        event="config-inited",
        callback=_config_inited,
        priority=-999,
    )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
