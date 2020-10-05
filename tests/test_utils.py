from xml.parsers.expat import ExpatError

import pytest

from gazpacho.utils import format, match, recover_html_and_attrs, sanitize


def test_attr_match():
    a = {"foo": "bar"}
    b = {"foo": "bar"}
    assert match(a, b)


def test_attr_match_query_empty():
    a = {}
    b = {"foo": "bar"}
    assert match(a, b)


def test_match_empty_empty():
    a = {}
    b = {}
    assert match(a, b)


def test_match_empty_attrs_fail():
    a = {"foo": "bar"}
    b = {}
    assert not match(a, b)


def test_match_partial():
    a = {"foo": "bar"}
    b = {"foo": "bar baz"}
    assert match(a, b, partial=True)


def test_match_multiple():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "bar2"}
    assert match(a, b)


def test_match_multiple_fail():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "baz1"}
    assert not match(a, b)


def test_match_query_too_much_fail():
    a = {"foo1": "bar1 baz1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "bar2"}
    assert not match(a, b)


def test_match_multiple_partial():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1 baz1", "foo2": "bar2"}
    assert match(a, b, partial=True)


def test_multiple_partial_fail():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1 baz1", "foo2": "bar2"}
    assert not match(a, b, partial=False)


def test_recover_html_and_attrs():
    html, attrs = recover_html_and_attrs("img", [("src", "example.png")])
    assert html == '<img src="example.png">' and attrs == {"src": "example.png"}


def test_format():
    html = """<ul><li>Item</li><li>Item</li></ul>"""
    assert format(html) == "<ul>\n  <li>Item</li>\n  <li>Item</li>\n</ul>"


def test_format_fail():
    html = """<div><ul><li>Item</li><li>Item</li></ul>"""
    with pytest.raises(ExpatError):
        format(html, fail=True)


def test_sanitize_weird_characters():
    url = sanitize("https://httpbin.org/anything/drãke")
    assert url == "https://httpbin.org/anything/dr%C3%A3ke"


def test_sanitize_missing_protocol():
    url = sanitize("gazpacho.xyz")
    assert url == "http://gazpacho.xyz"
