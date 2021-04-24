<<<<<<< HEAD
import pytest
=======
import json
from json.decoder import JSONDecodeError

import pytest

from gazpacho.get import HTTPError, UrllibHTTPError, get


def test_get(create_mock_responses):
    title = "<title>Gazpacho - Wikipedia"
    create_mock_responses(title, "application/text")
    url = "https://en.wikipedia.org/wiki/Gazpacho"

    content = get(url)
    if title not in content:
        raise AssertionError
>>>>>>> b2e870de2639ba21c9929e6ab966c6e532cc74b8

from gazpacho.get import HTTPError, get


def test_get():
    url = "https://en.wikipedia.org/wiki/Gazpacho"
    content = get(url)
    assert "<title>Gazpacho - Wikipedia" in content


def test_get_headers():
    url = "https://httpbin.org/headers"
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers = {"User-Agent": UA}
    content = get(url, headers=headers)
    if UA != content["headers"]["User-Agent"]:
        raise AssertionError


def test_get_multiple_headers():
    url = "https://httpbin.org/headers"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
    content = get(url, headers=headers)
    headers_set = set(headers.values())
<<<<<<< HEAD
    respeonse_set = set(content["headers"].values())
    assert headers_set.intersection(respeonse_set) == {"Mozilla/5.0", "gzip"}
=======
    response_set = set(content["headers"].values())
    if headers_set.intersection(response_set) != {"Mozilla/5.0", "gzip"}:
        raise AssertionError
>>>>>>> b2e870de2639ba21c9929e6ab966c6e532cc74b8


def test_get_params():
    url = "https://httpbin.org/anything"
    params = {"foo": "bar", "bar": "baz"}
    content = get(url, params)
    if params != content["args"]:
        raise AssertionError


def test_HTTPError_404():
    url = "https://httpstat.us/404"
    with pytest.raises(HTTPError):
        get(url)
