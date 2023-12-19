from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from eumdac.collection import Collection, SearchResults
from eumdac.errors import EumdacError, eumdac_raise_for_status
from eumdac.product import Product
from eumdac.request import get, post
from eumdac.token import AccessToken, URLs
from eumdac.logging import logger
import eumdac.common

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import Optional

    if sys.version_info < (3, 9):
        from typing import Iterable, Mapping
    else:
        from collections.abc import Iterable, Mapping


class DataStore:
    token: AccessToken
    urls: URLs
    _collections: Mapping[str, Collection]

    def __init__(self, token: AccessToken) -> None:
        self.token = token
        self.urls = token.urls
        self._collections = {}

    def _load_collections(self) -> None:
        if self._collections:
            return
        url = self.urls.get("datastore", "browse collections")
        response = get(
            url,
            params={"format": "json"},
            auth=self.token.auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status("Load collections failed", response, DataStoreError)
        collection_ids = [item["title"] for item in response.json()["links"]]
        self._collections = {
            collection_id: Collection(collection_id, self) for collection_id in collection_ids
        }

    @property
    def collections(self) -> Iterable[Collection]:
        self._load_collections()
        return list(self._collections.values())

    def get_collection(self, collection_id: str) -> Collection:
        """collection factory"""
        return Collection(collection_id, self)

    def check_collection_id(self, collection_id: str) -> None:
        """Used to validate the existence of a collection"""
        url = self.urls.get("datastore", "browse collection", vars={"collection_id": collection_id})
        response = None
        try:
            response = get(url, auth=self.token.auth, headers=eumdac.common.headers)
        except Exception as err:
            logger.error(f"Could not verify collection id due to {err}")

        if response and (
            response.status_code == 401
            or response.status_code == 403
            or response.status_code == 404
        ):
            eumdac_raise_for_status(
                "The collection you are searching for does not exist or you do not have authorisation to access it",
                response,
                CollectionNotFoundError,
            )

    def get_product(self, collection_id: str, product_id: str) -> Product:
        """product factory"""
        return Product(collection_id, product_id, self)

    def opensearch(self, query: str) -> SearchResults:
        q = self._parse_opensearchquery(query)
        if not "pi" in q:
            raise DataStoreError(
                "Please provide a Collection ID via the pi query parameter (i.e. pi=EO:EUM:DAT:MSG:HRSEVIRI)"
            )
        c = Collection(q.pop("pi"), self)
        return c.search(**q)

    def _parse_opensearchquery(self, query: str) -> dict[str, str]:
        query_dict = {}
        for member in query.split("&"):
            items = member.split("=")
            if len(items) != 2:
                raise DataStoreError(f"Invalid query member: {member}")
            if items[0] not in ["format", "si", "c", "id", "pw"] and items[0] is not None:
                query_dict[items[0]] = items[1]
        return query_dict


class DataStoreError(EumdacError):
    "Errors related to the DataStore"


class CollectionNotFoundError(EumdacError):
    """Error that will be raised when a collection does not exist"""
