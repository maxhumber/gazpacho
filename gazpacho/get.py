import json
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import urlencode
from urllib.request import build_opener

from .utils import sanitize, HTTPError
from typing import Dict, Optional, Union


def get(
    url: str,
    params: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Union[
    Dict[str, Dict[str, str]], Dict[str, Optional[Union[Dict[str, str], str]]], str
]:
    """Return the contents from a URL

    Params:

    - url (str): Target website URL
    - params (dict, optional): Param payload to add to the GET request
    - headers (dict, optional): Headers to add to the GET request

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
        UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
        opener.addheaders = [("User-Agent", UA)]
    try:
        with opener.open(url) as response:
            content = response.read().decode("utf-8")
            if response.headers.get_content_type() == "application/json":
                content = json.loads(content)
    except UrllibHTTPError as e:
        raise HTTPError(e.code, e.msg) from None
    return content
