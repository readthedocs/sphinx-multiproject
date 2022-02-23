from sharedconf.utils import get_docset

extensions = [
    "sharedconf.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
]

master_doc = "index"

sharedconf_docsets = {
    "api": {},
    "dev": {},
    "user": {},
}

docset = get_docset(sharedconf_docsets)

if docset == "api":
    language = "en"
    suppress_warnings = ["ref.doc"]
    locale_dirs = ["locale/api"]
elif docset == "dev":
    language = "es"
    suppress_warnings = ["ref.python"]
elif docset == "user":
    language = "de"
    locale_dirs = ["locale/api"]
