import json
from typing import Any

import click

import ckanext.search_schema.types as types
import ckanext.search_schema.adapters as adapter
from ckanext.search_schema.adapters import connect, SearchEngineType
from ckanext.search_schema.exceptions import SolrApiError


@click.group(short_help="search_schema command line interface")
def search_schema():
    """search_schema command line interface"""
    pass


@search_schema.command()
def definition():
    """Get a full schema definition"""
    conn: SearchEngineType = adapter.connect()
    click.echo(json.dumps(conn.get_full_schema(), indent=4))


@search_schema.command()
@click.argument("field_type", required=False)
def field_types(field_type: str):
    """Get a list of all field types. If field_type is provided, return an info
    about a specific field_type"""
    conn: SearchEngineType = adapter.connect()

    try:
        field_types: types.SolrApiFieldTypes = conn.get_field_types(field_type)
    except SolrApiError as e:
        return click.secho(e, fg="red")

    click.echo(json.dumps(field_types, indent=4))


@search_schema.command()
@click.argument("field_name")
def field(field_name: str):
    """Get a specific field definition"""
    conn: SearchEngineType = adapter.connect()
    click.echo(json.dumps(conn.get_field(field_name), indent=4))


def get_commands():
    return [search_schema]
