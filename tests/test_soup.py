import pytest
from gazpacho.soup import Soup


@pytest.fixture
def fake_html_1():
    html = """\
    <div class="foo" id="bar">
      <p>'IDK!'</p>
      <br/>
      <div class='baz'>
        <div>
          <span>Hi</span>
        </div>
      </div>
      <p id='blarg'>Try for 2</p>
      <div class='baz'>Oh No!</div>
    </div>
    """
    return html


@pytest.fixture
def fake_html_2():
    html = """\
    <div id='a' class='foo'>
      <div id='b' class='foo'>
      <p>bar</p>
      </div>
    </div>
    <div id='c' class='foo foo-striped'>
      <span>baz</span>
    </div>
    """
    return html


@pytest.fixture
def fake_html_3():
    html = """\
    <div class="foo-list">
      <a class="foo" href="/foo/1">
        <div class="foo-image-container">
          <img src="hi.png">
        </div>
      </a>
      <a class="foo" href="/foo/2">
        <div class="foo-image-container">
          <img src="bye.jpg">
        </div>
      </a>
    </div>
    <img src='pip_install.gif'>
    """
    return html


@pytest.fixture
def fake_html_4():
    html = """\
    <div class="foo-list">
      <span>I like <b>soup</b> and I really like <i>cold</i> soup</span>
      <p>I guess hot soup is okay too</p>
    </div>
    """
    return html


@pytest.fixture
def fake_html_5():
    html = """\
    <div>
        <div id="hi">
            <div>Text is text</div>
        </div>
        <img src="test1.png">
        <img src="test2.png">
        <img src="test3.png" />
        <div id="hi">Bye</div>
        <div id="hi2">Gotcha</div>
    </div>
    """
    return html


@pytest.fixture
def fake_html_6():
    html = """\
    <div>
        <p id=1>A</p>
        <p id=2>B</p>
        <p id=3>C</p>
        <p id=4>D</p>
        <p id=5>E</p>
        <p id=6>F</p>
        <p id=7>G</p>
    </div>
    """
    return html


def test_find(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("span")
    assert str(result) == "<span>Hi</span>"


def test_find_first(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("p", mode="first")
    assert str(result) == "<p>'IDK!'</p>"


def test_find_with_attrs(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("p", {"id": "blarg"})
    assert str(result) == '<p id="blarg">Try for 2</p>'


def test_find_multiple(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("div", {"class": "baz"})
    assert len(result) == 2
    assert str(result[1]) == '<div class="baz">Oh No!</div>'


def test_find_text(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("p", {"id": "blarg"})
    assert result.text == "Try for 2"


def test_find_nested_groups(fake_html_2):
    soup = Soup(fake_html_2)
    results = soup.find("div", {"class": "foo"})
    assert len(results) == 2


def test_find_partial_false(fake_html_2):
    soup = Soup(fake_html_2)
    result = soup.find("div", {"class": "foo"}, partial=False, mode="all")
    assert len(result) == 1


def test_find_nested_empty_tag(fake_html_3):
    soup = Soup(fake_html_3)
    result = soup.find("a", {"class": "foo"})
    assert len(result) == 2


def test_find_mutliple_imgs(fake_html_3):
    soup = Soup(fake_html_3)
    middle = soup.find("img")[1]
    assert middle.attrs["src"] == "bye.jpg"


def test_strip(fake_html_4):
    soup = Soup(fake_html_4)
    result = soup.strip()
    assert (
        result == "I like soup and I really like cold soup I guess hot soup is okay too"
    )


def test_strip_keep_whitespace(fake_html_4):
    soup = Soup(fake_html_4)
    result = soup.strip(whitespace=False)
    assert (
        result
        == "    \n      I like soup and I really like cold soup\n      I guess hot soup is okay too\n    \n    "
    )


def test_find_no_match_first(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("a", mode="first")
    assert result == None


def test_find_no_match_all(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("a", mode="all")
    assert result == []


def test_find_no_match_auto(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find("a", mode="auto")
    assert result == None


def test_malformed_void_tags(fake_html_5):
    soup = Soup(fake_html_5)
    result = soup.find("img")
    assert len(result) == 3


def test_remove_tags_warning(fake_html_4):
    with pytest.warns(FutureWarning):
        soup = Soup(fake_html_4)
        soup.remove_tags()


def test_find_strict(fake_html_2):
    with pytest.warns(FutureWarning):
        soup = Soup(fake_html_2)
        soup.find("div", {"class": "foo"}, strict=True)


def test_soup_get_cls_method():
    soup = Soup.get("www.google.com")
    assert "<!doctype html>" in str(soup).lower()


def test_bad_mode_argument(fake_html_1):
    with pytest.raises(ValueError):
        soup = Soup(fake_html_1)
        soup.find("div", mode="bad")


def test_undocumented_random_mode(fake_html_6):
    soup = Soup(fake_html_6)
    pset = set([soup.find("p", mode="random").attrs["id"] for _ in range(10)])
    assert len(pset) > 1


def test_undocumented_last_mode(fake_html_6):
    soup = Soup(fake_html_6)
    assert soup.find("p", mode="last").text == "G"
