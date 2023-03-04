import ckan.plugins.toolkit as tk


def search_schema_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "search_schema_required": search_schema_required,
    }
