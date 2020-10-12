import json
from typing import Any, Dict, Optional, Union
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import urlencode
from urllib.request import build_opener

from ..utils import HTTPError, sanitize

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:80.0) Gecko/20100101 Firefox/80.0"
)


def get(
    url: str,
    params: Dict[str, Any] = {},
    headers: Dict[str, Any] = {},
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
    opener.addheaders = list({**{"User-Agent": USER_AGENT}, **headers}.items())
    if params:
        url += "?" + urlencode(params)
    try:
        with opener.open(url) as response:
            content = response.read().decode("utf-8")
            if response.headers.get_content_type() == "application/json":
                content = json.loads(content)
    except UrllibHTTPError as e:
        raise HTTPError(e.code, e.msg) from None  # type: ignore
    return content
