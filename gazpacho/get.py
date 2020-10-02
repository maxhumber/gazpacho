import json
from typing import Optional, Union
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import quote, urlencode, urlsplit, urlunsplit
from urllib.request import build_opener


class HTTPError(Exception):
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"{self.code} - {self.msg}"


def sanitize(url: str) -> str:
    """\
    Sanitize and format a URL

    Arguments:

    - url: target page
    """
    scheme, netloc, path, query, fragment = urlsplit(url)
    if not scheme:
        scheme, netloc, path, query, fragment = urlsplit(f"http://{url}")
    path = quote(path)
    url = urlunsplit((scheme, netloc, path, query, fragment))
    return url


def get(
    url: str,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> Union[str, dict]:
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
        UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:80.0) Gecko/20100101 Firefox/80.0"
        opener.addheaders = [("User-Agent", UA)]
    try:
        with opener.open(url) as response:
            content = response.read().decode("utf-8")
            if response.headers.get_content_type() == "application/json":
                content = json.loads(content)
    except UrllibHTTPError as e:
        raise HTTPError(e.code, e.msg) from None  # type: ignore
    return content
