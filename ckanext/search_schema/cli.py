import json
import logging
from typing import Any

import click
from pygments import highlight, lexers, formatters

import ckanext.search_schema.const as const
import ckanext.search_schema.types as types
import ckanext.search_schema.facades as facade
from ckanext.search_schema.facades import SearchEngineType
from ckanext.search_schema.exceptions import SolrApiError


log = logging.getLogger(__name__)


@click.group(short_help="search_schema command line interface")
def search_schema():
    """search_schema command line interface"""
    pass


@search_schema.command()
@click.option(
    "-n",
    "--no-reindex",
    is_flag=True,
    help="Skip reindex after creating schema.",
)
def create(no_reindex: bool):
    """Populate a schema with required fields."""
    conn: SearchEngineType = facade.connect()
    conn.create_schema()

    if no_reindex:
        return

    log.info("Schema has been created. Reindexing...")
    conn.reindex()


@search_schema.command()
@click.argument(
    "group", type=click.Choice(const.SOLR_FIELD_GROUPS), required=False
)
def clear(group: str):
    """Clear a defined schema. Provide a target to clear a specific field group"""
    conn: SearchEngineType = facade.connect()
    conn.clear_schema([group] if group else const.SOLR_FIELD_GROUPS)


@search_schema.command()
def check():
    """Check if a schema is properly configured"""
    conn: SearchEngineType = facade.connect()
    check_result: dict[str, dict[str, Any]] = conn.check_schema()

    if not check_result:
        return click.secho("The schema is properly configured.", fg="green")

    _echo_colorized(json.dumps(check_result, indent=4))
    click.secho("There are some problems in your schema definition.", fg="red")
    click.secho(
        "Consider running "
        + click.style("ckan search-schema create", fg="green")
    )


@search_schema.command()
def definition():
    """Get a full search schema definition."""

    conn: SearchEngineType = facade.connect()

    _echo_colorized(json.dumps(conn.get_full_schema(), indent=4))


@search_schema.command()
@click.argument("field_type", required=False)
def field_types(field_type: str):
    """Get a list of all field types. If field_type is provided, return an info
    about a specific field_type"""
    conn: SearchEngineType = facade.connect()

    try:
        field_types = conn.get_field_types(field_type)
    except SolrApiError as e:
        return click.secho(e, fg="red")

    _echo_colorized(json.dumps(field_types, indent=4))


@search_schema.command()
@click.argument("field_name", required=False)
def fields(field_name: str):
    """Get a list of all fields. If field_name is provided, return an info
    about a specific field"""
    conn: SearchEngineType = facade.connect()

    try:
        fields: list[types.SolrField] | types.SolrField = conn.get_fields(
            field_name
        )
    except SolrApiError as e:
        return click.secho(e, fg="red")

    _echo_colorized(json.dumps(fields, indent=4))


@search_schema.command()
@click.argument("field_name", required=False)
def dynamic_fields(field_name: str):
    """Get a list of all dynamic fields. If field_name is provided, return an info
    about a specific field"""
    conn: SearchEngineType = facade.connect()
    try:
        fields = conn.get_dynamic_fields(field_name)
    except SolrApiError as e:
        return click.secho(e, fg="red")
    _echo_colorized(json.dumps(fields, indent=4))


@search_schema.command()
@click.argument("field_name", required=False)
def copy_fields(field_name: str):
    """Get a list of all fields. If field_name is provided, return an info
    about a specific field"""
    conn: SearchEngineType = facade.connect()

    try:
        fields = conn.get_copy_fields(field_name)
    except SolrApiError as e:
        return click.secho(e, fg="red")

    _echo_colorized(json.dumps(fields, indent=4))


@search_schema.command()
def template():
    """Get a basic search schema template"""
    click.secho("Not implemented yet.", fg="red")


def _echo_colorized(json_data: str):
    """Colorize JSON output with pygments library"""
    click.echo(
        highlight(
            json_data,
            lexers.JsonLexer(),
            formatters.TerminalFormatter(),
        )
    )


def get_commands():
    return [search_schema]
