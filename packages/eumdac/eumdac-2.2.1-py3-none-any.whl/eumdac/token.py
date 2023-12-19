"""Module containing classes to handle the token authentication."""
from __future__ import annotations

import abc
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import quote as url_quote

import requests
from importlib import resources as importlib_resources
from requests.auth import AuthBase, HTTPBasicAuth

from eumdac.request import post
import eumdac.common

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional

    if sys.version_info < (3, 9):
        from typing import Iterable, Mapping
    else:
        from collections.abc import Iterable, Mapping


class URLs(ConfigParser):
    def __init__(self, inifile: Optional[str] = None) -> None:
        super().__init__()
        if inifile:
            self.read(inifile)
        else:
            if hasattr(importlib_resources, "as_file"):  # python > 3.9
                with importlib_resources.as_file(
                    importlib_resources.files("eumdac") / "endpoints.ini"
                ) as path:
                    self.read(path)
            else:  # python < 3.9
                with importlib_resources.path("eumdac", "endpoints.ini") as path:
                    self.read(path)

    def get(  # type: ignore[override]
        self,
        section: str,
        option: str,
        raw: bool = False,
        vars: Optional[Mapping[str, str]] = None,
        fallback: str = "",
    ) -> str:
        if vars is not None:
            vars = {k: url_quote(str(v).encode()).replace("%", "%%") for k, v in vars.items()}
        return super().get(section, option, raw=raw, vars=vars, fallback=fallback)


class Credentials(NamedTuple):
    consumer_key: str
    consumer_secret: str


class HTTPBearerAuth(AuthBase):
    """Attaches HTTP Bearer Authentication to the given Request object.

    Attributes:
        token: Bearer token

    Arguments:
        token: Bearer token
    """

    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers["authorization"] = f"Bearer {self.token}"
        return request


class BaseToken(metaclass=abc.ABCMeta):
    urls: URLs

    @property
    def auth(self) -> Optional[AuthBase]:
        # overload in subclasses
        pass


class AccessToken(BaseToken):
    """Eumetsat API access token.

    Used to handle requesting of API tokens and there refreshment after expiration.

    Attributes:
        request_margin: seconds before expiration to start re-requesting
        expires_in: seconds before token expiration
        access_token: the value of the access token

    Arguments:
        cache (default: true): if true, use data from previous request until expiration
    """

    request_margin: int = 15  # seconds
    _expiration: int = 0
    _access_token: str = ""

    credentials: Credentials
    urls: URLs
    cache: bool

    def __init__(
        self,
        credentials: Iterable[str],
        cache: bool = True,
        urls: Optional[URLs] = None,
    ) -> None:
        self.credentials = Credentials(*credentials)
        self.urls = urls or URLs()
        self.cache = cache

    def __str__(self) -> str:
        return self.access_token

    @property
    def expiration(self) -> datetime:
        """Expiration of the current token string"""
        # Generate a token only when uninitialized
        if self._expiration == 0:
            self._update_token_data()
        return datetime.fromtimestamp(self._expiration)

    @property
    def access_token(self) -> str:
        """Token string"""
        expires_in = self._expiration - time.time()
        if not self.cache or expires_in < self.request_margin:
            self._update_token_data()
        return self._access_token

    @property
    def auth(self) -> AuthBase:
        return HTTPBearerAuth(self.access_token)

    def _update_token_data(self) -> None:
        auth = HTTPBasicAuth(*self.credentials)
        now = time.time()
        response = post(
            self.urls.get("token", "token"),
            auth=auth,
            data={"grant_type": "client_credentials"},
            headers=eumdac.common.headers,
        )
        response.raise_for_status()
        token_data = response.json()
        self._expiration = now + token_data["expires_in"]
        self._access_token = token_data["access_token"]


class AnonymousAccessToken(BaseToken):
    def __init__(self, urls: Optional[URLs] = None):
        self.urls = urls or URLs()

    @property
    def auth(self) -> Optional[AuthBase]:
        return None
