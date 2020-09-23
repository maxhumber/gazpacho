from typing import Any, Dict, List, Tuple, Union
from urllib.parse import quote, urlsplit, urlunsplit


def match(a: dict, b: dict, *, partial: bool = False) -> bool:
    """Match two dictionaries

    Params:

    - a: query dict
    - b: dict to match
    - partial: allow partial match

    Examples:

    ```
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b, partial=True)
    # True

    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b)
    # False

    a = {}
    b = {'foo': 'bar'}
    match(a, b)
    # True

    a = {}
    b = {}
    match(a, b)
    # True
    ```
    """
    if (not a) or (not a and not b):
        return True
    if a and (not b):
        return False
    for key, value in a.items():
        if not b.get(key):
            return False
        if not partial:
            if value == b.get(key):
                continue
            else:
                return False
        if value in b.get(key):
            continue
        else:
            return False
    return True


def recover_html_and_attrs(
    tag: str, attrs: List[Tuple[str, str]], startendtag: bool = False
) -> Tuple[str, Dict[str, str]]:
    """Reconstruct html and attrs from HTMLParser

    Arguments:

    - tag: element tag
    - attrs: attributes as a list of tuples
    - startendtag: flag for start-end tags

    Example:

    ```
    recover_html_and_attrs('img', [('src', 'example.png')])
    # ("<img src='example.png'>", {'src': 'example.png'})
    ```
    """
    if attrs:
        attrs = dict(attrs)
        af = [f'{key}="{value}"' for key, value in attrs.items()]
        af = f' {" ".join(af)}'
    else:
        attrs = {}
        af = ""
    if startendtag:
        html = f"<{tag}{af} />"
    else:
        html = f"<{tag}{af}>"
    return html, attrs


def sanitize(url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    if not scheme:
        scheme, netloc, path, query, fragment = urlsplit(f"http://{url}")
    path = quote(path)
    url = urlunsplit((scheme, netloc, path, query, fragment))
    return url


class HTTPError(Exception):
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"{self.code} - {self.msg}"
