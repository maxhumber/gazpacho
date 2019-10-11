from gazpacho import match


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
    assert match(a, b)


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
    assert match(a, b)


def test_multiple_strict_fail():
    a = {"foo1": "bar1", "foo2": "bar2"}
    b = {"foo1": "bar1 baz1", "foo2": "bar2"}
    assert not match(a, b, strict=True)
