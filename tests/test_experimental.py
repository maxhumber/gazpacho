import pytest
from gazpacho import get, Soup
from gazpacho.experimental import find_block, extract_tag_and_attrs, similar

@pytest.fixture
def fake_html_1():
    html = """\
        <div>
            <img src="hi.png">
            <div class="price">$19.99</div>
            <div class="price">$5.00</div>
            <div class="price-reduced">$2.99</div>
            <div>Not a price</div>
            <div><p>$100.05 CAD</p></div>
            <div>
                <p>$200 USD</p>
            </div>
        </div>
    """
    return html


def test_find_block_not_nested(fake_html_1):
    html = fake_html_1
    target = "$19.99"
    result = find_block(target, html)
    assert result == '<div class="price">$19.99</div>'


def test_find_block_nested_line(fake_html_1):
    html = fake_html_1
    target = "$100.05 CAD"
    block = find_block(target, html)
    assert block == '<p>$100.05 CAD</p>'


def test_find_block_nested_newline(fake_html_1):
    html = fake_html_1
    target = "$200 USD"
    block = find_block(target, html)
    assert block == '<p>$200 USD</p>'


def test_extract_tag_no_attrs():
    block = '<div>$19.99</div>'
    tag, attrs = extract_tag_and_attrs(block)
    assert tag == "div" and attrs == {}


def test_extract_tag_one_attr():
    block = '<div class="price-reduced">$2.99</div>'
    tag, attrs = extract_tag_and_attrs(block)
    assert tag == 'div' and attrs == {'class': 'price-reduced'}


def test_extract_tag_and_multiple_weird_attrs():
    block = '<td class="tmx left" data-team="27" data-label="TEAM ▾">Toronto Pine Needles</td>'
    tag, attrs = extract_tag_and_attrs(block)
    assert tag == "td" and attrs == {'class': 'tmx left', 'data-team': '27', 'data-label': 'TEAM ▾'}


def test_similar_early_riser():
    html = get("https://scrape.world/books")
    target = "Early Riser"
    assert len(similar(target, html)) == 3


def test_escaped_string():
    html = get("https://scrape.world/books")
    target = "$15.99 CAD"
    assert len(similar(target, html)) == 3
