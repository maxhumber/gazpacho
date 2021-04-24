import json
from json.decoder import JSONDecodeError

import pytest

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
