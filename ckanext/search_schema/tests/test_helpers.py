"""Tests for helpers.py."""

import ckanext.search_schema.helpers as helpers


def test_search_schema_hello():
    assert helpers.search_schema_hello() == "Hello, search_schema!"
