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
    assert len(result) == 1
    assert str(result[0]) == '<span>Hi</span>'

def test_find_with_attrs(fake_html):
    soup = Soup(fake_html)
    result = soup.find('p', {'id': 'blarg'})
    assert len(result) == 1
    assert str(result[0]) == '<p id="blarg">Try for 2</p>'

def test_find_multiple(fake_html):
    soup = Soup(fake_html)
    result = soup.find('div', {'class': 'baz'})
    assert len(result) == 2


# from gazpacho import get, Soup
# url = 'https://en.wikipedia.org/wiki/Gazpacho'
# html = get(url)
# soup = Soup(html)
# soup.find('span', {'class': 'mw-headline'})
# # [<span class="mw-headline" id="History">History</span>,
# #  <span class="mw-headline" id="Ingredients_and_preparation">Ingredients and preparation</span>,
# #  <span class="mw-headline" id="Variations">Variations</span>,
# #  <span class="mw-headline" id="In_Spain">In Spain</span>,
# #  <span class="mw-headline" id="Arranque_roteño">Arranque roteño</span>,
# #  <span class="mw-headline" id="Extremaduran_variations">Extremaduran variations</span>,
# #  <span class="mw-headline" id="La_Mancha_variations">La Mancha variations</span>,
# #  <span class="mw-headline" id="Castilian_variations">Castilian variations</span>,
# #  <span class="mw-headline" id="See_also">See also</span>,
# #  <span class="mw-headline" id="References">References</span>]


# url = 'https://news.ycombinator.com/'
# html = get(url)
# soup = Soup(html)
# results = soup.find('tr', {'class': 'athing'})
# results[0].find('td', {'class': 'title'})[1]
#
# url = 'https://en.wikipedia.org/wiki/Fantasy_hockey'
#
# soup = Soup(html)
# soup.__dir__()
# results = soup.find('span', {'class': 'mw-headline'})
# results[0]
# results[0].data
#
# url = 'https://www.goodreads.com/quotes/search'
# params = {'commit': 'Search', 'page': 2, 'q': 'blake crouch'}
# html = get(url, params)
#
# soup = Soup(html)
# soup.find('a')
#
# results = soup.find('div', {'class': 'quoteText'})
# results
