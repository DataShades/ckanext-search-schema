"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.search_schema.logic import validators


def test_search_schema_reauired_with_valid_value():
    assert validators.search_schema_required("value") == "value"


def test_search_schema_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.search_schema_required(None)
