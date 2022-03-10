import os

from sphinx.util import logging

log = logging.getLogger(__name__)


def get_project(projects, env_var="PROJECT"):
    """
    Get the current docset.

    :param dict docsets: A dictionary of projects.
    :param str env_var: The env variable name from where to read
     the value of the current project.

    :returns: the name of the current project.
    """
    if not projects:
        log.error("`projects` can't be empty.")
        raise ValueError

    project_names = list(projects.keys())
    project = os.environ.get(env_var, project_names[0])
    if project not in project_names:
        log.error(
            "Project `%s` isn't valid. Valid values are: %s",
            project,
            ", ".join(project_names),
        )
        raise Exception
    return project
