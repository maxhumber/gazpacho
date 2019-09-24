import json
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



url = 'https://en.wikipedia.org/wiki/Fantasy_hockey'
html = get(url)
soup = Soup(html)
soup.__dir__()
results = soup.find('span', {'class': 'mw-headline'})
results[0]
results[0].data

url = 'https://www.goodreads.com/quotes/search'
params = {'commit': 'Search', 'page': 2, 'q': 'blake crouch'}
html = get(url, params)

soup = Soup(html)
soup.find('a')

results = soup.find('div', {'class': 'quoteText'})
results




#
