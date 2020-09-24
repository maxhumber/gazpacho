import pytest
from gazpacho.get import get, sanitize, HTTPError


def test_get():
    url = "https://en.wikipedia.org/wiki/Gazpacho"
    content = get(url)
    assert "<title>Gazpacho - Wikipedia" in content


def test_get_headers():
    url = "https://httpbin.org/headers"
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers = {"User-Agent": UA}
    content = get(url, headers=headers)
    assert UA == content["headers"]["User-Agent"]


def test_get_params():
    url = "https://httpbin.org/anything"
    params = {"foo": "bar", "bar": "baz"}
    content = get(url, params)
    assert params == content["args"]


def test_HTTPError_404():
    url = "https://httpstat.us/404"
    with pytest.raises(HTTPError):
        get(url)


def test_sanitize_weird_characters():
    url = sanitize("https://httpbin.org/anything/drãke")
    assert url == "https://httpbin.org/anything/dr%C3%A3ke"


def test_sanitize_missing_protocol():
    url = sanitize("gazpacho.xyz")
    assert url == "http://gazpacho.xyz"
