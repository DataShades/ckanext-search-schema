import ckan.plugins.toolkit as tk
import ckanext.search_schema.logic.schema as schema


@tk.side_effect_free
def search_schema_get_sum(context, data_dict):
    tk.check_access(
        "search_schema_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.search_schema_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'search_schema_get_sum': search_schema_get_sum,
    }
