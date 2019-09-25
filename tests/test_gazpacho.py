import json
import pytest
from gazpacho import *

def test_get():
    url = 'https://en.wikipedia.org/wiki/Gazpacho'
    content = get(url)
    assert '<title>Gazpacho - Wikipedia' in content

def test_get_headers():
    url = 'https://httpbin.org/headers'
    headers = {'User-Agent': DEFAULT_USER_AGENT}
    content = get(url, headers=headers)
    user_agent = json.loads(content)['headers']['User-Agent']
    assert user_agent == DEFAULT_USER_AGENT

def test_get_params():
    url = 'https://httpbin.org/anything'
    params = {'foo': 'bar', 'bar': 'baz'}
    content = get(url, params)
    args = json.loads(content)['args']
    assert args == params

def test_match_empty():
    d1 = None
    d2 = {'foo': 'bar'}
    assert match(d1, d2)

def test_match_exact():
    d1 = {'foo': 'bar'}
    d2 = {'foo': 'bar'}
    assert match(d1, d2)

def test_match_complete():
    d1 = {'foo': 'bar'}
    d2 = {'foo': 'bar', 'bar': 'baz'}
    assert match(d1, d2)

def test_match_partial():
    d1 = {'foo': 'bar'}
    d2 = {'foo': 'bar baz'}
    assert match(d1, d2)

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
