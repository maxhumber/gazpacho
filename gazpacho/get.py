from urllib.parse import urlencode
from urllib.request import build_opener


def get(url, params=None, headers=None):
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
    opener = build_opener()
    if params:
        url += "?" + urlencode(params)
    if headers:
        for h in headers.items():
            opener.addheaders = [h]
    if (headers and not headers.get("User-Agent")) or not headers:
        UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        opener.addheaders = [("User-Agent", UA)]
    with opener.open(url) as f:
        content = f.read().decode("utf-8")
    return content
