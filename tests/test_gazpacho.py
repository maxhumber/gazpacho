import json
import pytest
from gazpacho import *

def test_get():
    url = 'https://en.wikipedia.org/wiki/Gazpacho'
    content = get(url)
    assert '<title>Gazpacho - Wikipedia' in content

def test_get_headers():
    url = 'https://httpbin.org/headers'
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'
    headers = {'User-Agent': UA}
    content = get(url, headers=headers)
    user_agent = json.loads(content)['headers']['User-Agent']
    assert user_agent == UA

def test_get_params():
    url = 'https://httpbin.org/anything'
    params = {'foo': 'bar', 'bar': 'baz'}
    content = get(url, params)
    args = json.loads(content)['args']
    assert args == params

def test_attr_match():
    a = {'foo': 'bar'}
    b = {'foo': 'bar'}
    assert match(a, b)

def test_attr_match_query_empty():
    a = {}
    b = {'foo': 'bar'}
    assert match(a, b)

def test_match_empty_empty():
    a = {}
    b = {}
    assert match(a, b)

def test_match_empty_attrs_fail():
    a = {'foo': 'bar'}
    b = {}
    assert not match(a, b)

def test_match_partial():
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    assert match(a, b)

def test_match_multiple():
    a = {'foo1': 'bar1', 'foo2': 'bar2'}
    b = {'foo1': 'bar1', 'foo2': 'bar2'}
    assert match(a, b)

def test_match_multiple_fail():
    a = {'foo1': 'bar1', 'foo2': 'bar2'}
    b = {'foo1': 'bar1', 'foo2': 'baz1'}
    assert not match(a, b)

def test_match_query_too_much_fail():
    a = {'foo1': 'bar1 baz1', 'foo2': 'bar2'}
    b = {'foo1': 'bar1', 'foo2': 'bar2'}
    assert not match(a, b)

def test_match_multiple_partial():
    a = {'foo1': 'bar1', 'foo2': 'bar2'}
    b = {'foo1': 'bar1 baz1', 'foo2': 'bar2'}
    assert match(a, b)

def test_multiple_strict_fail():
    a = {'foo1': 'bar1', 'foo2': 'bar2'}
    b = {'foo1': 'bar1 baz1', 'foo2': 'bar2'}
    assert not match(a, b, strict=True)

@pytest.fixture
def fake_html():
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

def test_find_one(fake_html):
    soup = Soup(fake_html)
    result = soup.find('span')
    assert str(result) == '<span>Hi</span>'

def test_find_with_attrs(fake_html):
    soup = Soup(fake_html)
    result = soup.find('p', {'id': 'blarg'})
    assert str(result) == '<p id="blarg">Try for 2</p>'

def test_find_multiple(fake_html):
    soup = Soup(fake_html)
    result = soup.find('div', {'class': 'baz'})
    assert len(result) == 2
    assert str(result[1]) == '<div class="baz">Oh No!</div>'

def test_find_text(fake_html):
    soup = Soup(fake_html)
    result = soup.find('p', {'id': 'blarg'})
    assert result.text == 'Try for 2'
