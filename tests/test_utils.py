import pytest

from sharedconf.utils import get_docset


class TestGetDocSet:
    def test_empty_docsets(self):
        with pytest.raises(ValueError):
            get_docset({})

    def test_invalid_docset(self, monkeypatch):
        monkeypatch.setenv("DOCSET", "notfound")
        with pytest.raises(Exception):
            get_docset({"docs": {}})

    def test_get_docset(self, monkeypatch):
        monkeypatch.setenv("DOCSET", "dev")
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_docset(docsets)
        assert docset == "dev"

    def test_default_docset_first_item(self, monkeypatch):
        monkeypatch.delenv("DOCSET", raising=False)
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_docset(docsets)
        assert docset == "api"

    def test_custom_env_name(self, monkeypatch):
        monkeypatch.setenv("DOCSET", "dev")
        monkeypatch.setenv("MYDOCSET", "user")
        docsets = {
            "api": {},
            "dev": {},
            "user": {},
        }
        docset = get_docset(docsets, env_var="MYDOCSET")
        assert docset == "user"
