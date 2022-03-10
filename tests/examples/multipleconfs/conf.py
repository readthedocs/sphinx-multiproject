extensions = [
    "multiproject.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
]

master_doc = "index"

multiproject_projects = {
    "api": {},
    "dev": {},
    "user": {
        "config": {
            "project": "Override",
            "suppress_warnings": ["ref.python"],
        }
    },
}
