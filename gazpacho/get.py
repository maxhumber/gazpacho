import json
import random
from typing import Any, Dict, Union
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import urlencode
from urllib.request import build_opener

from .utils import HTTPError, sanitize

USER_AGENT = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:80.0) Gecko/20100101 Firefox/80.0",
    "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3"
]


def random_ua(string):
    list_length = len(string)
    agent = random.randrange(list_length)
    random_agent = string[agent]
    return random_agent


def get(
    url: str,
    params: Dict[str, Any] = None,
    headers: Dict[str, Any] = None,
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
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    url = sanitize(url)
    opener = build_opener()
    opener.addheaders = list({**{"User-Agent": random_ua(USER_AGENT)}, **headers}.items())
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
