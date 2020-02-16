import json
import pytest
from gazpacho import get


def test_get():
    url = "https://en.wikipedia.org/wiki/Gazpacho"
    content = get(url)
    assert "<title>Gazpacho - Wikipedia" in content


def test_get_headers():
    url = "https://httpbin.org/headers"
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers = {"User-Agent": UA}
    content = get(url, headers=headers)
    user_agent = json.loads(content)["headers"]["User-Agent"]
    assert user_agent == UA


def test_get_params():
    url = "https://httpbin.org/anything"
    params = {"foo": "bar", "bar": "baz"}
    content = get(url, params)
    args = json.loads(content)["args"]
    assert args == params


def test_weird_characters():
    url = 'https://httpbin.org/anything/drãke'
    content = get(url)
    assert url == json.loads(content)['url']
