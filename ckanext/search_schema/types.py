from __future__ import annotations

from typing import Optional, TypedDict, Literal


SolrFieldGroups = Literal[
    "copy-field",
    "dynamic-field",
    "field",
    "field-type",
]


class SolrSchema(TypedDict):
    name: str
    version: float | int
    uniqueKey: str
    fieldTypes: list["SolrFieldType"]
    fields: list["SolrField"]
    dynamicFields: list["SolrDynamicField"]
    copyFields: list["SolrCopyField"]


SolrFieldType = TypedDict(
    "SolrFieldType",
    {
        "name": str,
        "class": str,
        "omitTermFreqAndPositions": Optional[bool],
        "omitNorms": Optional[bool],
        "indexed": Optional[bool],
        "stored": Optional[bool],
        "required": Optional[bool],
        "multiValued": Optional[bool],
        "docValues": Optional[bool],
        "large": Optional[bool],
        "useDocValuesAsStored": Optional[bool],
        "maxCharsForDocValues": Optional[str],
        "positionIncrementGap": Optional[str],
        "autoGeneratePhraseQueries": Optional[str],
        "synonymQueryStyle": Optional[str],
        "enableGraphQueries": Optional[bool],
        "docValuesFormat": Optional[str],
        "postingsFormat": Optional[str],
        "uninvertible": Optional[bool],
        "indexAnalyzer": Optional[dict[str, dict[str, str]]],
        "queryAnalyzer": Optional[dict[str, dict[str, str]]],
        "analyzer": Optional[dict[str, dict[str, str]]],
        "geo": Optional[str],
        "maxDistErr": Optional[str],
        "termOffsets": Optional[bool],
        "termPositions": Optional[bool],
        "termVectors": Optional[bool],
        "termPayloads": Optional[bool],
        "omitPositions": Optional[bool],
        "distErrPct": Optional[str],
        "distanceUnits": Optional[str],
        "subFieldSuffix": Optional[str],
        "dimension": Optional[str],
    },
)


class SolrField(TypedDict):
    name: str
    type: str
    default: Optional[str]
    omitTermFreqAndPositions: Optional[bool]
    omitNorms: Optional[bool]
    indexed: Optional[bool]
    stored: Optional[bool]
    required: Optional[bool]
    multiValued: Optional[bool]
    docValues: Optional[bool]
    large: Optional[bool]
    useDocValuesAsStored: Optional[bool]
    sortMissingFirst: Optional[bool]
    sortMissingLast: Optional[bool]
    uninvertible: Optional[bool]
    omitPositions: Optional[bool]
    termVectors: Optional[bool]
    termPositions: Optional[bool]
    termOffsets: Optional[bool]
    termPayloads: Optional[bool]


class SolrDynamicField(SolrField):
    pass


class SolrCopyField(TypedDict):
    source: str
    dest: str


SolrSchemaDefinition = TypedDict(
    "SolrSchemaDefinition",
    {
        "copy-field": list[SolrCopyField],
        "dynamic-field": list[SolrDynamicField],
        "field": list[SolrField],
        "field-type": list[SolrFieldType],
    },
    total=False
)
