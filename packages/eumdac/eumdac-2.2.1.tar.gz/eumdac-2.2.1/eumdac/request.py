import json
import random
from types import TracebackType
import requests
import time

from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Any, Callable, Dict

from eumdac.errors import EumdacError
from eumdac.logging import logger


class RequestError(EumdacError):
    """Error for requests"""

    pass


class RetryAndLog(Retry):
    def increment(
        self,
        method: Any = None,
        url: Any = None,
        response: Any = None,
        error: Any = None,
        _pool: Any = None,
        _stacktrace: Any = None,
    ) -> Retry:
        target_uri = ""
        if _pool:
            target_uri = f"{method} {_pool.scheme}://{_pool.host}:{_pool.port}{url}"
        elif error:
            target_uri = f"{error.conn.host}{url}"

        cause = ""
        if response and response.data:
            cause = f'server response {response.status} - "{response.data}" '
        if error:
            cause = f'{cause}error: "{error}"'

        logger.info(f"Trying again for {target_uri} due to {cause}")
        return super().increment(method, url, response, error, _pool, _stacktrace)


def _get_adapter(max_retries: int, backoff_factor: float) -> HTTPAdapter:
    retry = RetryAndLog(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH"],
        raise_on_status=False,
    )

    return HTTPAdapter(max_retries=retry)


def _should_retry(response: requests.Response, backoff: int = random.randint(1, 6) * 10) -> bool:
    if response.status_code == 429:
        rd = json.loads(response.text)
        # handle throttling
        message = rd["message"]["reason"]
        if "message" in rd and "retryAfter" in rd["message"]:
            # Traffic limits exceeded
            timestamp = int(rd["message"]["retryAfter"]) / 1000
            utc_endtime = datetime.utcfromtimestamp(timestamp)
            duration = utc_endtime - datetime.utcnow()
            if duration.total_seconds() > 0:
                logger.warning(f"{rd['message']}: operation will resume in {duration}")
                time.sleep(duration.total_seconds())
                return True
        elif "message" in rd and "reason" in rd["message"]:
            if rd["message"]["reason"] == "Maximum number of connections exceeded":
                # Maximum number of connections exceeded
                logger.warning(f"{message}: throttling for {backoff}s")
                time.sleep(backoff)
                return True
            elif rd["message"]["reason"] == "Maximum number of requests exceeded":
                # Maximum number of requests exceeded
                logger.warning(f"{message}: throttling for 1s")
                time.sleep(1)
                return True

    return False


def _request(
    method: str,
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 0.3,
    **kwargs: Any,
) -> requests.Response:
    adapter = _get_adapter(max_retries, backoff_factor)
    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = requests.Response()
    try:
        while True:
            if hasattr(session, method):
                logger.debug(pretty_print(method, url, kwargs))
                response = getattr(session, method.lower())(url, **kwargs)
                if _should_retry(response):
                    continue
            else:
                raise RequestError(f"Operation not supported: {method}")
            break
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Received unexpected response: {e}")
    except requests.exceptions.RetryError as e:
        raise RequestError(
            f"Maximum retries ({max_retries}) reached for {method.capitalize()} {url}"
        )

    return response


def get(url: str, **kwargs: Any) -> requests.Response:
    return _request("get", url, **kwargs)


def post(url: str, **kwargs: Any) -> requests.Response:
    return _request("post", url, **kwargs)


def patch(url: str, **kwargs: Any) -> requests.Response:
    return _request("patch", url, **kwargs)


def put(url: str, **kwargs: Any) -> requests.Response:
    return _request("put", url, **kwargs)


def delete(url: str, **kwargs: Any) -> requests.Response:
    return _request("delete", url, **kwargs)


def pretty_print(method: str, url: str, kwargs: Dict[str, Any]) -> str:
    pargs = dict(kwargs)
    if "headers" in pargs:
        pargs["headers"].pop("referer", None)
        pargs["headers"].pop("User-Agent", None)
        if len(pargs["headers"]) == 0:
            pargs.pop("headers")
    if "auth" in pargs:
        if hasattr(pargs["auth"], "token"):
            pargs["auth"] = f"Bearer {str(pargs['auth'].token)}"
        else:
            pargs["auth"] = f"{type(pargs['auth']).__name__}"
    return f"Request: {method.upper()} {url}, payload: {pargs}"
