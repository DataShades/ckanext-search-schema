from ckan.plugins.interfaces import Interface

from ckanext.search_schema.types import SolrSchemaDefinition


class ISearchSchema(Interface):
    """Interface to modify schema definition before create it"""

    def update_search_schema_definitions(
        self, definitions: SolrSchemaDefinition
    ):
        """Accepts a schema definition that could be altered before schema
        will be created. The plugin accepts the responsibility of providing valid
        definition according to SOLR syntax"""
        pass
