"""
This module defines errors and error handling functions for eumdac.
"""
import json
from typing import *
from urllib.parse import urlparse

import requests


def eumdac_raise_for_status(
    msg: str, response: requests.Response, exc_cls: Type[Exception]
) -> None:
    """take a message and a requests response to transform it into a eumdac error."""
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        url = urlparse(response.url)
        response_text = response.text
        if not response_text and response.raw:
            response_text = response.raw.data
        try:
            extra_info = json.loads(response_text)
        except json.decoder.JSONDecodeError:
            extra_info = {"text": response_text}
        extra_info.update({"url": url, "status": response.status_code})
        if response.status_code > 500:
            msg += " (due to a server-side error)"
        exception = exc_cls(msg, extra_info)
        raise exception from exc


class EumdacError(Exception):
    """All eumdac errors will inherit from a EumdacError"""

    def __init__(self, msg: str, extra_info: Optional[Dict[str, Any]] = None):
        self.extra_info = extra_info
        if extra_info:
            if "title" in extra_info:
                msg = f"{msg} - {extra_info['title']}"
            if "description" in extra_info:
                msg = f"{msg}. {extra_info['description']}"
        super().__init__(msg)
