from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Optional, TypeAlias
from urllib.parse import urlparse, urlunparse, ParseResult

from requests import request, RequestException, Response

from ckan.plugins import toolkit as tk

from ckanext.search_schema import const
from ckanext.search_schema.exceptions import SolrAdapterError, SolrApiError


class SearchEngineAdapter(ABC):
    def _send_request(
        self, url, params=None, data=None, headers=None, method="GET"
    ) -> dict[str, Any]:
        try:
            response: Response = request(
                method, url, params=params, data=data, headers=headers
            )
            response.raise_for_status()
        except RequestException as e:
            raise Exception(f"Error executing request to {url}: {e}")
        return json.loads(response.content)

    @abstractmethod
    def _get_url(self, endpoint: str) -> str:
        pass

    @abstractmethod
    def get_full_schema(self) -> str:
        pass

    @abstractmethod
    def get_field_types(
        self, field_type: Optional[str]
    ) -> list[dict[str, Any]] | dict[str, Any]:
        pass

    @abstractmethod
    def get_field(self, field_name: str) -> dict[str, Any]:
        pass


class SolrBaseAdapter(SearchEngineAdapter):
    def __init__(
        self, base_url: Optional[str] = None, collection: Optional[str] = None
    ):
        self.solr_url: str = tk.config.get(const.SOLR_URL)

        if not self.solr_url:
            raise SolrAdapterError("The solr_url is missing from configuration")

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
            raise SolrAdapterError("The solr_url doesn't contain collection")

        return collection

    def _get_url(self, endpoint: str) -> str:
        """Build a url to endpoint"""
        return f"{self.base_url}/solr/{self.collection}/{endpoint}"


class Solr5Adapter(SolrBaseAdapter):
    """An adapter for Solr 5+"""

    def query(
        self, collection, query, fields=None, filters=None, sort=None, start=0, rows=10
    ):
        url = self._get_url(f"{collection}/select")
        params = {"q": query, "start": start, "rows": rows, "wt": "json"}
        if fields:
            params["fl"] = fields
        if filters:
            params["fq"] = filters
        if sort:
            params["sort"] = sort
        return self._send_request(url, params=params)

    def add(self, collection, documents):
        headers = {"Content-type": "application/json"}
        data = json.dumps({"add": documents})
        return self._send_request(
            self._get_url("/update"), data=data, headers=headers, method="POST"
        )

    def delete(self, collection, query=None):
        headers = {"Content-type": "application/json"}
        if query:
            data = json.dumps({"delete": {"query": query}})
        else:
            data = json.dumps({"delete": {"query": "*:*"}})
        return self._send_request(
            self._get_url("update"), data=data, headers=headers, method="POST"
        )

    def commit(self, collection):
        headers = {"Content-type": "application/json"}
        data = json.dumps({"commit": {}})
        return self._send_request(
            self._get_url("update"), data=data, headers=headers, method="POST"
        )

    def optimize(self, collection):
        url = self._get_url("update")
        headers = {"Content-type": "application/json"}
        data = json.dumps({"optimize": {}})
        return self._send_request(url, data=data, headers=headers, method="POST")

    def get_full_schema(self) -> dict[str, Any]:
        return self._send_request(
            self._get_url("schema"),
            params={"wt": "json"},
        )

    def get_field_types(
        self, field_type: Optional[str] = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        url: str = (
            self._get_url("schema/fieldtypes")
            if not field_type
            else self._get_url(f"schema/fieldtypes/{field_type}")
        )

        resp: dict[str, Any] = self._send_request(
            url,
            params={"wt": "json"},
        )

        return resp["fieldTypes"] if not field_type else resp["fieldType"]

    def get_field(self, field_name: str) -> dict[str, Any]:
        resp: dict[str, Any] = self._send_request(
            self._get_url(f"schema/fields/{field_name}"),
            params={"wt": "json"},
        )
        import ipdb

        ipdb.set_trace()
        return resp


class Solr8Adapter(SolrBaseAdapter):
    """An adapter for Solr 8+"""

    def get_full_schema(self) -> str:
        return self._send_request(
            self._get_url("schema"),
            params={"wt": "json"},
        )["schema"]

    def get_field_types(
        self, field_type: Optional[str]
    ) -> list[dict[str, Any]] | dict[str, Any]:
        # ['name', 'version', 'uniqueKey', 'fieldTypes', 'fields', 'dynamicFields', 'copyFields']
        resp: dict[str, Any] = self._send_request(
            self._get_url("schema"),
            params={"wt": "json"},
        )

        if not field_type:
            return resp["schema"]["fieldTypes"]

        for field_type_metadata in resp["schema"]["fieldTypes"]:
            if field_type_metadata["name"] == field_type:
                return field_type_metadata

        raise SolrApiError(f"field_type {field_type} doesn't exist")

    def get_field(self, field_name: str) -> dict[str, Any]:
        return {}


class ElasticSearchAdapter(SearchEngineAdapter):
    """TODO"""

    def _get_url(self, endpoint: str) -> str:
        return ""

    def get_full_schema(self) -> str:
        return ""

    def get_field_types(
        self, field_type: Optional[str]
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return {}

    def get_field(self, field_name: str) -> dict[str, Any]:
        return {}


SearchEngineType: TypeAlias = Solr5Adapter | Solr8Adapter | ElasticSearchAdapter


def connect() -> Solr5Adapter | Solr8Adapter | ElasticSearchAdapter:
    """Return an adapter of current search engine"""
    return Solr8Adapter()
