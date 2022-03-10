import pytest

from multiproject.utils import get_project


class TestGetDocSet:
    def test_empty_docsets(self):
        with pytest.raises(ValueError):
            get_project({})

    def test_invalid_docset(self, monkeypatch):
        monkeypatch.setenv("PROJECT", "notfound")
        with pytest.raises(Exception):
            get_project({"docs": {}})

    def test_get_docset(self, monkeypatch):
        monkeypatch.setenv("PROJECT", "dev")
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_project(docsets)
        assert docset == "dev"

    def test_default_docset_first_item(self, monkeypatch):
        monkeypatch.delenv("PROJECT", raising=False)
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_project(docsets)
        assert docset == "api"

    def test_custom_env_name(self, monkeypatch):
        monkeypatch.setenv("PROJECT", "dev")
        monkeypatch.setenv("MYDOCSET", "user")
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_project(docsets, env_var="MYDOCSET")
        assert docset == "user"
