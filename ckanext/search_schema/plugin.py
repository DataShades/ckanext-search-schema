import ckan.plugins as plugins

import ckanext.search_schema.cli as cli


class SearchSchemaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)

    # IClick

    def get_commands(self):
        return cli.get_commands()
