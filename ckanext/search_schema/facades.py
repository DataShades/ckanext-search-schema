from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, TypeAlias
from urllib.parse import urlparse, urlunparse, ParseResult

from requests import request, RequestException, Response

from ckan.plugins import toolkit as tk

import ckanext.search_schema.types as t
from ckanext.search_schema import const
from ckanext.search_schema.exceptions import SolrConfigError, SolrApiError


log = logging.getLogger(__name__)


class SolrFacade(ABC):
    def _send_request(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        method: str = "GET",
    ) -> dict[str, Any]:
        headers = headers or {}
        headers["Content-Type"] = "application/json"

        try:
            response: Response = request(
                method, url, params=params, json=data, headers=headers
            )
            response.raise_for_status()
        except RequestException as e:
            raise Exception(f"Error executing request to {url}: {e}")
        return response.json()

    @abstractmethod
    def _get_url(self, endpoint: str) -> str:
        pass

    @abstractmethod
    def get_full_schema(self) -> t.SolrSchema:
        pass

    @abstractmethod
    def get_field_types(
        self, field_type: Optional[str]
    ) -> list[t.SolrFieldType]:
        pass

    @abstractmethod
    def get_fields(self, field_name: str) -> list[t.SolrField]:
        pass

    @abstractmethod
    def get_copy_fields(self, field_name: str) -> list[t.SolrCopyField]:
        pass

    @abstractmethod
    def get_dynamic_fields(self, field_name: str) -> list[t.SolrDynamicField]:
        pass

    @abstractmethod
    def clear_schema(self, groups: t.SolrFieldGroups):
        pass


class SolrBaseFacade(SolrFacade):
    def __init__(
        self, base_url: Optional[str] = None, collection: Optional[str] = None
    ):
        self.solr_url: str = tk.config.get(const.SOLR_URL)

        if not self.solr_url:
            raise SolrConfigError("The solr_url is missing from configuration")

        self.base_url: str = base_url or self._get_base_url_from_config()
        self.collection: str = collection or self._get_collection_from_config()

    def _get_base_url_from_config(self) -> str:
        """Parse a base_url from a configured solr_url"""
        result: ParseResult = urlparse(self.solr_url)
        return urlunparse([result.scheme, result.netloc, "", "", "", ""])

    def _get_collection_from_config(self) -> str:
        """Parse a collection from a configured solr_url"""
        result: ParseResult = urlparse(self.solr_url)
        collection: str = result.path.strip("/").split("/")[1]

        if not collection:
            raise SolrConfigError("The solr_url doesn't contain collection")

        return collection

    def _get_url(self, endpoint: str) -> str:
        """Build a url to endpoint"""
        return f"{self.base_url}/solr/{self.collection}/{endpoint}"

    def get_full_schema(self) -> t.SolrSchema:
        return self._send_request(
            self._get_url("schema"),
            params={"wt": "json"},
        )["schema"]

    def get_field_types(
        self, field_type: Optional[str]
    ) -> list[t.SolrFieldType]:
        """Return a list of defined field types"""
        return self._get_field(const.SOLR_F_TYPE, field_type)

    def get_fields(self, field_name: str) -> list[t.SolrField]:
        """Return a list of defined fields"""
        return self._get_field(const.SOLR_FIELD, field_name)

    def get_copy_fields(self, field_name: str) -> list[t.SolrCopyField]:
        """Return a list of defined copy fields"""
        return self._get_field(const.SOLR_COPY_FIELD, field_name)

    def get_dynamic_fields(self, field_name: str) -> list[t.SolrDynamicField]:
        """Return a list of defined dynamic fields"""
        return self._get_field(const.SOLR_DYN_FIELD, field_name)

    def _get_field(self, group: str, field_name: Optional[str]):
        schema: t.SolrSchema = self.get_full_schema()

        if not field_name:
            return schema[group]

        for entity_metadata in schema[group]:
            if entity_metadata["name"] == field_name:
                return [entity_metadata]

        raise SolrApiError(f"{group} `{field_name}` doesn't exist")


class Solr5Facade(SolrBaseFacade):
    def clear_schema(self, groups: t.SolrFieldGroups):
        pass


class Solr8Facade(SolrBaseFacade):
    def clear_schema(self, groups: t.SolrFieldGroups):
        """Clear a SOLR schema for provided groups"""
        schema: t.SolrSchema = self.get_full_schema()
        data: dict[str, list[dict[str, str]]] = {}

        for group in groups:
            key: str = const.SOLR_GROUP_MAPPING[group]
            command: str = f"delete-{group}"
            data.setdefault(command, [])

            if not schema[key]:
                continue

            log.info(f"Solr schema API. Clearing SOLR {key} group")

            if group == "copy-field":
                data[command].extend(schema[key])
            else:
                fields = [
                    {"name": field["name"]}
                    for field in schema[key]
                    if field["name"]
                    not in const.SOLR_FIXED_FIELDS.get(group, [])
                ]
                data[command].extend(fields)

        self._send_request(self._get_url("schema"), data=data, method="post")

        log.info(f"Solr schema API. Schema has been cleared")


# class ElasticSearchFacade():
#     """TODO"""

#     def _get_url(self, endpoint: str) -> str:
#         return ""

#     def get_full_schema(self) -> str:
#         return ""

#     def get_field_types(
#         self, field_type: Optional[str]
#     ) -> list[t.SolrFieldType]:
#         return {}

#     def get_fields(self, field_name: str) -> dict[str, Any]:
#         return {}


SearchEngineType: TypeAlias = Solr5Facade | Solr8Facade


def connect() -> SearchEngineType:
    """Return a facade class of current search engine"""
    return Solr8Facade()
