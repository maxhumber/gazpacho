import pytest
from gazpacho import Soup

@pytest.fixture
def fake_html_1():
    html = '''<div class="foo" id="bar">
      <p>'IDK!'</p>
      <br/>
      <div class='baz'>
        <div>
          <span>Hi</span>
        </div>
      </div>
      <p id='blarg'>Try for 2</p>
      <div class='baz'>Oh No!</div>
    </div>'''
    return html

@pytest.fixture
def fake_html_2():
    html = '''<div id='a' class='foo'>
      <div id='b' class='foo'>
      <p>bar</p>
      </div>
    </div>
    <div id='c' class='foo foo-striped'>
      <span>baz</span>
    </div>'''
    return html

def test_find_one(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find_one('span')
    assert str(result) == '<span>Hi</span>'

def test_find_one_with_find(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find('span')
    assert str(result) == '[<span>Hi</span>]'

def test_find_one_with_attrs(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find_one('p', {'id': 'blarg'})
    assert str(result) == '<p id="blarg">Try for 2</p>'

def test_find_multiple(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find('div', {'class': 'baz'})
    assert len(result) == 2
    assert str(result[1]) == '<div class="baz">Oh No!</div>'

def test_find_text(fake_html_1):
    soup = Soup(fake_html_1)
    result = soup.find_one('p', {'id': 'blarg'})
    assert result.text == 'Try for 2'

def test_find_nested_groups(fake_html_2):
    soup = Soup(fake_html_2)
    results = soup.find('div', {'class': 'foo'})
    assert len(results) == 2

def test_find_strict(fake_html_2):
    soup = Soup(fake_html_2)
    result = soup.find('div', {'class': 'foo'}, strict=True)
    assert len(result) == 1
