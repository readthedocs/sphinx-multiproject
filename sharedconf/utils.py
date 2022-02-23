import os

from sphinx.util import logging

log = logging.getLogger(__name__)


def get_docset(docsets, env_var="DOCSET"):
    """
    Get the current docset.

    :param dict docsets: A dictionary of docsets.
    :param str env_var: The env variable name from where to read
     the value of the current docset.

    :returns: the name of the current docset.
    """
    if not docsets:
        log.error("`docsets` can't be empty.")
        raise ValueError

    docset_names = list(docsets.keys())
    docset = os.environ.get(env_var, docset_names[0])
    if docset not in docset_names:
        log.error(
            "Docset `%s` isn't valid. Valid values are: %s",
            docset,
            ", ".join(docset_names),
        )
        raise Exception
    return docset
