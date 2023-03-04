"""Tests for views.py."""

import pytest

import ckanext.search_schema.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "search_schema")
@pytest.mark.usefixtures("with_plugins")
def test_search_schema_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("search_schema.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, search_schema!"
