from multiproject.utils import get_project

extensions = [
    "multiproject.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
]

master_doc = "index"

multiproject_projects = {
    "api": {},
    "dev": {},
    "user": {},
}

current_project = get_project(multiproject_projects)

if current_project == "api":
    language = "en"
    suppress_warnings = ["ref.doc"]
    locale_dirs = ["locale/api"]
elif current_project == "dev":
    language = "es"
    suppress_warnings = ["ref.python"]
elif current_project == "user":
    language = "de"
    locale_dirs = ["locale/api"]
