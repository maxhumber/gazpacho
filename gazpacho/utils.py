from urllib.parse import quote, urlsplit, urlunsplit

import functools
import warnings

def deprecated_alias(**aliases):
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            rename_kwargs(f.__name__, kwargs, aliases)
            return f(*args, **kwargs)
        return wrapper
    return deco

def rename_kwargs(func_name, kwargs, aliases):
    for alias, new in aliases.items():
        if alias in kwargs:
            if new in kwargs:
                raise TypeError(f'{func_name} received both {alias} and {new}')
            warnings.warn(f'{alias} is deprecated; use {new}', DeprecationWarning)
            kwargs[new] = kwargs.pop(alias)

@deprecated_alias(strict='partial')
def match(a, b, partial=True, *, strict=None):
    """Utility function to match two dictionaries

    Params:

    - a (dict): Query dictionary
    - b (dict): Dictionary to match
    - strict (bool): Require exact matching

    Examples:

    ```
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b)
    # True

    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b, strict=True)
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
    if strict:
        partial = not strict
    if not a:
        return True
    if not a and not b:
        return True
    if a and not b:
        return False
    for key, value in a.items():
        if not b.get(key):
            return False
        if strict:
            if value == b.get(key):
                continue
            else:
                return False
        if value in b.get(key):
            continue
        else:
            return False
    return True


match(a={'foo': 'bar'}, b={'foo': 'bar baz'}, partial)


def html_starttag_and_attrs(tag, attrs, startendtag=False):
    """Utility functon to reconstruct starttag and attrs

    Params:

    - tag (str): HTML element tag
    - attrs (list): HTML element attributes formatted as a list of tuples
    - startendtag (bool, False): Flag to handle startend tags

    Example:

    ```
    html_starttag_and_attrs('a', [('href', 'localhost:8000')])
    # ('<a href="localhost:8000">', {'href': 'localhost:8000'})
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


def sanitize(url):
    scheme, netloc, path, query, fragment = urlsplit(url)
    if not scheme:
        scheme, netloc, path, query, fragment = urlsplit(f"http://{url}")
    path = quote(path)
    url = urlunsplit((scheme, netloc, path, query, fragment))
    return url


class HTTPError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"{self.code} - {self.msg}"
