import json
from urllib.error import HTTPError as UnderlyingError
from urllib.parse import quote, urlencode, urlsplit, urlunsplit
from urllib.request import build_opener


class HTTPError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.message = msg

    def __str__(self):
        return f"{self.code} - {self.message}"


class URL:
    def __init__(self, url, params={}):
        self._url = url
        self._params = params
        if not url.startswith("http://") or not url.startswith("https://"):
            url = f"http://{url}"
        scheme, netloc, path, query, fragment = urlsplit(url)
        path = quote(path)
        self.scheme = scheme
        self.netloc = netloc
        self.path = path
        self.fragment = fragment
        if params:
            self.query = urlencode(params)
        else:
            self.query = query

    def __repr__(self):
        return f"{self.url}"

    @property
    def params(self):
        if self._params:
            return self._params
        else:
            return dict(parse.parse_qsl(self.query))

    @property
    def url(self):
        return urlunsplit(
            (self.scheme, self.netloc, self.path, self.query, self.fragment)
        )


class Opener:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"

    def __init__(self, headers={}, encoding="utf-8"):
        self.opener_director = build_opener()
        self._headers = headers
        self.encoding = encoding

    @property
    def headers(self):
        headers = {**{"User-Agent": self.USER_AGENT}, **self._headers}
        return list(headers.items())

    def read(self, url):
        opener = self.opener_director
        opener.addheaders = self.headers
        with opener.open(str(url)) as r:
            content = r.read().decode(self.encoding)
            if r.headers.get_content_type() == "application/json":
                content = json.loads(content)
        return content


def get(url, params={}, *, headers={}, encoding="utf-8"):
    """Retrieve the contents of a URL

    Params:

    - url (str): target
    - params (dict): GET request payload
    - headers (dict): GET request headers
    - encoding (str): content encoding

    Returns:

    - str/dict/None

    Example:

    ```
    get("https://httpbin.org/anything", {"soup": "gazpacho"})
    ```
    """
    url = URL(url, params)
    opener = Opener(headers, encoding)
    try:
        return opener.read(url)
    except UnderlyingError as e:
        raise HTTPError(e.code, e.msg) from None
