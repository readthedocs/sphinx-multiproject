from pathlib import Path

from sphinx import version_info
from sphinx.util import logging

from . import __version__, utils

log = logging.getLogger(__name__)


def _get_docset_from_config(config):
    docset = utils.get_docset(config.sharedconf_docsets, config.sharedconf_env_var)
    return docset, config.sharedconf_docsets[docset]


def _override_srdir(app, config):
    """
    Override app.srcdir with the value from the current docset.

    If the docset doesn't have a path,
    the name of the docset is used as the path.

    Values can be absolute or relative to the original source dir.
    """
    docset, options = _get_docset_from_config(config)
    log.info("Using docset: %s", docset)

    original_srcdir = Path(app.srcdir)
    new_srcdir = Path(options.get("path", docset))
    if not new_srcdir.is_absolute():
        new_srcdir = original_srcdir / new_srcdir
    app.srcdir = str(new_srcdir.resolve())


def _override_config(config):
    """Override the config with specific values from the current docset."""
    docset, options = _get_docset_from_config(config)
    docset_config = options.get("config", {})
    # Taken from
    # https://github.com/sphinx-doc/sphinx/blob/586de7300a5269de93b4d813408ffdbf10ce2409/sphinx/config.py#L222-L222
    pre_init_options = {"needs_sphinx", "suppress_warnings", "language", "locale_dirs"}
    for option, value in docset_config.items():
        if option in pre_init_options:
            log.warning(
                "Setting the `%s` option inside the docset won't have the desired effect. "
                "Please see https://sphinx-sharedconf.readthedocs.io/page/limitation.html",
                option,
            )
        config[option] = value


def _config_inited(app, config):
    _override_srdir(app, config)
    _override_config(config)


def setup(app):
    app.add_config_value(
        "sharedconf_env_var",
        default="DOCSET",
        rebuild="env",
        types=[str],
    )
    app.add_config_value(
        "sharedconf_docsets",
        default={},
        rebuild="env",
        types=[dict],
    )

    kwargs = {
        "event": "config-inited",
        "callback": _config_inited,
    }
    if version_info >= (3, 0):
        # Priority should be as low as possible, so other extensions that
        # depend on the srcdir or the docset config use the new value.
        kwargs["priority"] = -999
    app.connect(**kwargs)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
