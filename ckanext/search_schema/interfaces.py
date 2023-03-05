from ckan.plugins.interfaces import Interface


class ISearchSchema(Interface):
    """Interface to modify schema definition before create it"""
    def update_search_schema_definitions(self):
        pass
