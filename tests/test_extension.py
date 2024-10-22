from unittest import mock

import pytest
from sphinx import version_info as sphinx_version

# Sphinx versions previous to 7.2 used a custom
# Path class for the srcdir in tests, while newer versions
# use a plain Path class.
if sphinx_version >= (7, 2, 0):
    from pathlib import Path
else:
    from sphinx.testing.path import path as Path

basedir = Path(__file__).parent / "examples"


class TestExtension:
    @pytest.mark.sphinx("html", srcdir=basedir / "basic")
    def test_build_default_project(self, app):
        assert list(app.config.multiproject_projects.keys())[0] == "api"
        app.build()
        expected_srcdir = basedir / "basic/api"
        assert app.srcdir == str(expected_srcdir)
        out = (Path(app.outdir) / "index.html").read_text()
        assert "API documentation" in out

    @pytest.mark.parametrize(
        "project, expected_text",
        [
            ("api", "API documentation"),
            ("dev", "Dev documentation"),
            ("user", "User documentation"),
        ],
    )
    def test_build_project(self, make_app, monkeypatch, project, expected_text):
        monkeypatch.setenv("PROJECT", project)
        app = make_app("html", srcdir=basedir / "basic")
        app.build()
        expected_srcdir = basedir / "basic" / project
        assert app.srcdir == str(expected_srcdir)
        out = (Path(app.outdir) / "index.html").read_text()
        assert expected_text in out

    def test_per_projec_settings(self, make_app):
        config = {
            "project": "A project",
            "multiproject_projects": {
                "dev": {
                    "config": {
                        "project": "Dev documentation",
                    },
                },
            },
        }
        app = make_app("html", srcdir=basedir / "basic", confoverrides=config)
        app.build()

        assert app.config.project == "Dev documentation"

        out = (Path(app.outdir) / "index.html").read_text()
        assert "Dev documentation" in out

    def test_custom_project_path(self, make_app):
        config = {
            "multiproject_projects": {
                "dev": {
                    "path": "user",
                },
            },
        }
        app = make_app("html", srcdir=basedir / "basic", confoverrides=config)
        app.build()

        out = (Path(app.outdir) / "index.html").read_text()
        assert "User documentation" in out

    def test_custom_env_var(self, make_app, monkeypatch):
        monkeypatch.setenv("PROJECT", "dev")
        monkeypatch.setenv("MYDOCSET", "user")
        config = {"multiproject_env_var": "MYDOCSET"}
        app = make_app("html", srcdir=basedir / "basic", confoverrides=config)
        app.build()

        expected_srcdir = basedir / "basic/user"
        assert app.srcdir == str(expected_srcdir)

        out = (Path(app.outdir) / "index.html").read_text()
        assert "User documentation" in out

    @mock.patch("multiproject.extension.log")
    def test_warn_special_settings(self, log, make_app):
        config = {
            "language": "en",
            "multiproject_projects": {
                "dev": {
                    "use_config_file": False,
                    "config": {
                        "language": "es",
                    },
                },
            },
        }
        app = make_app("html", srcdir=basedir / "basic", confoverrides=config)
        app.build()

        assert app.config.language == "es"

        log.warning.assert_called_once()
        args, _ = log.warning.call_args
        assert args[0].startswith("Setting the `%s` option from the extension")
        assert args[1] == "language"

    @pytest.mark.parametrize(
        "project, expected_text, expected_config",
        [
            (
                "api",
                "API documentation",
                {
                    "language": "en",
                    "suppress_warnings": ["ref.doc"],
                    "locale_dirs": ["locale/api"],
                },
            ),
            (
                "dev",
                "Dev documentation",
                {
                    "language": "es",
                    "suppress_warnings": ["ref.python"],
                    "locale_dirs": ["locales"],
                },
            ),
            (
                "user",
                "User documentation",
                {
                    "language": "de",
                    "suppress_warnings": [],
                    "locale_dirs": ["locale/api"],
                },
            ),
        ],
    )
    def test_conditional_settings(
        self, make_app, monkeypatch, project, expected_text, expected_config
    ):
        monkeypatch.setenv("PROJECT", project)
        app = make_app("html", srcdir=basedir / "conditional")
        app.build()

        expected_srcdir = basedir / "conditional" / project
        assert app.srcdir == str(expected_srcdir)

        out = (Path(app.outdir) / "index.html").read_text()
        assert expected_text in out

        for k, v in expected_config.items():
            assert app.config[k] == v

    @pytest.mark.parametrize(
        "project, expected_text, expected_config",
        [
            (
                "api",
                "API documentation",
                {
                    "master_doc": "index",
                    "project": "API",
                },
            ),
            (
                "dev",
                "Dev documentation",
                {
                    "master_doc": "index",
                    "project": "Dev",
                },
            ),
            (
                "user",
                "User documentation",
                {
                    "project": "User",
                    "suppress_warnings": ["ref.python"],
                },
            ),
        ],
    )
    def test_using_config_file(
        self, make_app, monkeypatch, project, expected_text, expected_config
    ):
        monkeypatch.setenv("PROJECT", project)
        app = make_app("html", srcdir=basedir / "multipleconfs")
        app.build()

        expected_srcdir = basedir / "multipleconfs" / project
        assert app.srcdir == str(expected_srcdir)

        out = (Path(app.outdir) / "index.html").read_text()
        assert expected_text in out

        for k, v in expected_config.items():
            assert app.config[k] == v

    def test_not_using_config_file(self, make_app, monkeypatch):
        monkeypatch.setenv("PROJECT", "user")
        config = {
            "project": "A project",
            "multiproject_projects": {
                "user": {
                    "use_config_file": False,
                    "config": {
                        "project": "Override",
                    },
                },
            },
        }
        assert (basedir / "multipleconfs/user/conf.py").exists()
        app = make_app("html", srcdir=basedir / "multipleconfs", confoverrides=config)
        app.build()

        assert app.config.project == "Override"

        out = (Path(app.outdir) / "index.html").read_text()
        assert "User documentation" in out
