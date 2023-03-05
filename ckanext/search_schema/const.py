SOLR_URL = "solr_url"
SOLR_F_TYPE = "fieldTypes"
SOLR_FIELD = "fields"
SOLR_DYN_FIELD = "dynamicFields"
SOLR_COPY_FIELD = "copyFields"
SOLR_FIELD_GROUPS = [
    "copy-field",
    "dynamic-field",
    "field",
    "field-type",
]
SOLR_GROUP_MAPPING = {
    "copy-field": SOLR_COPY_FIELD,
    "dynamic-field": SOLR_DYN_FIELD,
    "field": SOLR_FIELD,
    "field-type": SOLR_F_TYPE,
}
SOLR_FIXED_FIELDS = {
    "field-type": [
        "text_general",
        "string",
        "booleans",
        "pdates",
        "plong",
        "plongs",
        "pdoubles",
    ],
    "field": ["id", "_version_"],
}
