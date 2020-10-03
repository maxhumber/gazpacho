import json
from typing import Any, Dict, Optional, Union
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import urlencode
from urllib.request import build_opener

from .utils import HTTPError, sanitize


def get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> Union[str, Dict[str, Any]]:
    """Retrive url contents

    Params:

    - url: target page
    - params: GET request payload
    - headers: GET request headers

    Example:

    ```
    get('https://httpbin.org/anything', {'soup': 'gazpacho'})
    ```
    """
    url = sanitize(url)
    opener = build_opener()
    if params:
        url += "?" + urlencode(params)
    if headers:
        for h in headers.items():
            opener.addheaders = [h]
    if (headers and not headers.get("User-Agent")) or not headers:
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:80.0) Gecko/20100101 Firefox/80.0"
        opener.addheaders = [("User-Agent", ua)]
    try:
        with opener.open(url) as response:
            content = response.read().decode("utf-8")
            if response.headers.get_content_type() == "application/json":
                content = json.loads(content)
    except UrllibHTTPError as e:
        raise HTTPError(e.code, e.msg) from None  # type: ignore
    return content
