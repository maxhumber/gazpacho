from xml.parsers.expat import ExpatError

import pytest

from gazpacho.utils import format, match, recover_html_and_attrs, sanitize


def test_attr_match():
    a = {"foo": "bar"}
    b = {"foo": "bar"}
    if not match(a, b):
        raise AssertionError


def test_attr_match_query_empty():
    a = {}
    b = {"foo": "bar"}
    if not match(a, b):
        raise AssertionError


def test_match_empty_empty():
    a = {}
    b = {}
    if not match(a, b):
        raise AssertionError


def test_match_empty_attrs_fail():
    a = {"foo": "bar"}
    b = {}
    if match(a, b):
        raise AssertionError


def test_match_partial():
    a = {"foo": "bar"}
    b = {"foo": "bar baz"}
    if not match(a, b, partial=True):
        raise AssertionError


def test_match_multiple():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "bar2"}
    if not match(a, b):
        raise AssertionError


def test_match_multiple_fail():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "baz1"}
    if match(a, b):
        raise AssertionError


def test_match_query_too_much_fail():
    a = {"foo1": "bar1 baz1", "foo2": "bar2"}
    b = {"foo1": "bar1", "foo2": "bar2"}
    if match(a, b):
        raise AssertionError


def test_match_multiple_partial():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1 baz1", "foo2": "bar2"}
    if not match(a, b, partial=True):
        raise AssertionError


def test_multiple_partial_fail():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1 baz1", "foo2": "bar2"}
    if match(a, b, partial=False):
        raise AssertionError


def test_recover_html_and_attrs():
    html, attrs = recover_html_and_attrs("img", [("src", "example.png")])
    if not (html == '<img src="example.png">' and attrs == {"src": "example.png"}):
        raise AssertionError


def test_format():
    html = """<ul><li>Item</li><li>Item</li></ul>"""
    if format(html) != "<ul>\n  <li>Item</li>\n  <li>Item</li>\n</ul>":
        raise AssertionError


def test_format_whitespace():
    html = """<ul>                <li>Item</li           ><li>Item</li>

    </ul       >"""
    if format(html) != "<ul>\n  <li>Item</li>\n  <li>Item</li>\n</ul>":
        raise AssertionError


def test_format_whitespace_inside_tag():
    html = """<ul><li>Item</li><li>I t e m</li></ul>"""
    if format(html) != "<ul>\n  <li>Item</li>\n  <li>I t e m</li>\n</ul>":
        raise AssertionError


def test_format_fail_missing_closing():
    with pytest.raises(ExpatError):
        html = """<div><ul><li>Item</li><li>Item</li></ul>"""
        format(html, fail=True)


def test_format_fail_closing_order():
    with pytest.raises(ExpatError):
        html = """<div><ul><li>Item</li><li>Item</li></div></ul>"""
        format(html, fail=True)


def test_format_leading_text():
    with pytest.raises(ExpatError):
        html = """Leading Text<ul><li>Item</li><li>Item</li></ul>"""
        format(html, fail=True)


def test_format_trailing_text():
    with pytest.raises(ExpatError):
        html = """<ul><li>Item</li><li>Item</li></ul>Trailing Text"""
        format(html, fail=True)


def test_format_void_tag():
    html = """<body><img src="self-closing.png"/><img src="void.png"></body>"""
    if (
        format(html) != """<body>\n  <img src="self-closing.png">\n  <img src="void.png">\n</body>"""
    ):
        raise AssertionError


def test_format_invalid_void_tag_fail():
    html = """<body><xxx src="void.png"></body>"""
    with pytest.raises(ExpatError):
        format(html, fail=True)


def test_sanitize_weird_characters():
    url = sanitize("https://httpbin.org/anything/drãke")
    if url != "https://httpbin.org/anything/dr%C3%A3ke":
        raise AssertionError


def test_sanitize_missing_protocol():
    url = sanitize("gazpacho.xyz")
    if url != "http://gazpacho.xyz":
        raise AssertionError
