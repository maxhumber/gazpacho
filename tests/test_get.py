import json
import sys
from json.decoder import JSONDecodeError
from unittest.mock import patch

import pytest
from gazpacho.get import HTTPError, UrllibHTTPError, build_opener, get


def test_get(create_mock_responses):
    title = "<title>Gazpacho - Wikipedia"
    create_mock_responses(title, "application/text")
    url = "https://en.wikipedia.org/wiki/Gazpacho"

    content = get(url)
    assert title in content


def test_get_invalid_content_type(create_mock_responses):
    create_mock_responses("asd")

    url = "https://en.wikipedia.org/wiki/Gazpacho"
    with pytest.raises(JSONDecodeError):
        get(url)


def test_get_headers(create_mock_responses):
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers = {"User-Agent": UA}
    create_mock_responses(json.dumps({"headers": headers}))
    url = "https://httpbin.org/headers"

    content = get(url, headers=headers)
    assert UA == content["headers"]["User-Agent"]


def test_get_multiple_headers(create_mock_responses):
    url = "https://httpbin.org/headers"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
    create_mock_responses(json.dumps({"headers": headers}))

    content = get(url, headers=headers)
    headers_set = set(headers.values())
    response_set = set(content["headers"].values())
    assert headers_set.intersection(response_set) == {"Mozilla/5.0", "gzip"}


def test_get_params(create_mock_responses):
    params = {"foo": "bar", "bar": "baz"}
    create_mock_responses(json.dumps({"args": params}))
    url = "https://httpbin.org/anything"

    content = get(url, params)
    assert params == content["args"]


def test_HTTPError_404(create_mock_responses):
    url = "https://httpstat.us/404"
    _, mock_response = create_mock_responses("asd")
    mock_response.headers.get_content_type.side_effect = UrllibHTTPError(
        url, 404, "Not found", None, None
    )
    with pytest.raises(HTTPError):
        get(url)
