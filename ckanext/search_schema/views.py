from flask import Blueprint


search_schema = Blueprint(
    "search_schema", __name__)


def page():
    return "Hello, search_schema!"


search_schema.add_url_rule(
    "/search_schema/page", view_func=page)


def get_blueprints():
    return [search_schema]
