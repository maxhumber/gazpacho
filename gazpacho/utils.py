from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote, urlsplit, urlunsplit


def match(a: Dict[Any, Any], b: Dict[Any, Any], *, partial: bool = False) -> bool:
    """Match two dictionaries

    Arguments:

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
    for key, lhs in a.items():
        rhs = b.get(key)
        if not rhs:
            return False
        if not partial:
            if lhs == rhs:
                continue
            else:
                return False
        if lhs in rhs:
            continue
        else:
            return False
    return True


def recover_html_and_attrs(
    tag: str, attrs: List[Tuple[str, Optional[str]]], startendtag: bool = False
) -> Tuple[str, Dict[str, str]]:
    """\
    Recover html and attrs from HTMLParser feed

    Arguments:

    - tag: element tag
    - attrs: element attributes
    - startendtag: if startend tag

    Example:

    ```
    recover_html_and_attrs('img', [('src', 'example.png')])
    # ("<img src='example.png'>", {'src': 'example.png'})
    ```
    """
    if attrs:
        attrs_dict = dict(attrs)
        attrs_list = [f'{key}="{value}"' for key, value in attrs_dict.items()]
        attrs_str = f' {" ".join(attrs_list)}'
    else:
        attrs_dict = {}
        attrs_str = ""
    if startendtag:
        html = f"<{tag}{attrs_str} />"
    else:
        html = f"<{tag}{attrs_str}>"
    return html, attrs_dict


def sanitize(url: str) -> str:
    """\
    TODO
    """
    scheme, netloc, path, query, fragment = urlsplit(url)
    if not scheme:
        scheme, netloc, path, query, fragment = urlsplit(f"http://{url}")
    path = quote(path)
    url = urlunsplit((scheme, netloc, path, query, fragment))
    return url


class HTTPError(Exception):
    """\
    TODO
    """

    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"{self.code} - {self.msg}"
