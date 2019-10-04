<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/images/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-zero-blueviolet"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pepy.tech/project/gazpacho"><img alt="Downloads" src="https://pepy.tech/badge/gazpacho"></a>  
</p>



#### About

gazpacho is a web scraping library. It replaces requests and BeautifulSoup for most projects. gazpacho is small, simple, fast, and consistent. You should use it!



#### Usage

gazpacho is easy to use. To retrieve the contents of a web page use `get`. And to parse the retrieved contents use `Soup`.



#### Get

The `get` function retrieves content from a web page:

```python
from gazpacho import get

url = 'https://en.wikipedia.org/wiki/Gazpacho'
html = get(url)
print(html[:50])

# <!DOCTYPE html>
# <html class="client-nojs" lang="en
```

The `get` function also accepts optional params and headers for any GET request.

```python
url = 'https://httpbin.org/anything'
get(url, params={'foo': 'bar', 'bar': 'baz'}, headers={'User-Agent': 'gazpacho'})
```



#### Soup

The `Soup` object takes an HTML string and turns it into something parsable:

```python
from gazpacho import Soup

soup = Soup(html)
str(soup)[:50]

# '<!DOCTYPE html>\n<html class="client-nojs" lang="en'
```

In order to parse an HTML element inside of a `Soup` object, pass the desired tag and attributes (optional) to the `find` method:

```python
# Original HTML: <span class="mw-headline" id="Ingredients_and_preparation">Ingredients and preparation</span>

results = soup.find('span', {'class': 'mw-headline'})
```

The `find` method will return a list of `Soup` objects for those elements that satisfy the tag and attribute constraints:

```python
print(results)

# [<span class="mw-headline" id="History">History</span>,
#  <span class="mw-headline" id="Ingredients_and_preparation">Ingredients and preparation</span>,
#  <span class="mw-headline" id="Variations">Variations</span>,
#  <span class="mw-headline" id="In_Spain">In Spain</span>,
#  <span class="mw-headline" id="Arranque_roteño">Arranque roteño</span>,
#  <span class="mw-headline" id="Extremaduran_variations">Extremaduran variations</span>,
#  <span class="mw-headline" id="La_Mancha_variations">La Mancha variations</span>,
#  <span class="mw-headline" id="Castilian_variations">Castilian variations</span>,
#  <span class="mw-headline" id="See_also">See also</span>,
#  <span class="mw-headline" id="References">References</span>]
```

Whereas `find` will return a list, the `find_one` method will return the first found element as a `Soup` object:

```python
soup.find_one('span', {'class': 'mw-headline'})
# <span class="mw-headline" id="History">History</span>
```

`Soup` objects returned by the `find` or `find_one` methods will have `html`, `tag`, `attrs`, and `text` attributes:

```python
result = results[3]
print(result.html)
# <span class="mw-headline" id="In_Spain">In Spain</span>
print(result.tag)
# span
print(result.attrs)
# {'class': 'mw-headline', 'id': 'In_Spain'}
print(result.text)
# In Spain
```

Importantly, returned `Soup` objects can reimplement the `find` and `find_one` methods!



#### Production

gazpacho is production ready. The library currently powers [quote](https://github.com/maxhumber/quote), a python wrapper for the Goodreads Quote API. And a fully worked example of gazpacho in action is available [here](https://maxhumber.com/scraping_fantasy_hockey). 



#### Comparison

gazpacho is a drop-in replacement for most projects that use requests and BeautifulSoup:

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.capfriendly.com/browse/active/2020/salary?p=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
df = pd.read_html(str(soup.find('table')))[0]
print(df[['PLAYER', 'TEAM', 'SALARY', 'AGE']].head(3))

#                PLAYER TEAM       SALARY  AGE
# 0  1. Mitchell Marner  TOR  $16,000,000   22
# 1  2. Auston Matthews  TOR  $15,900,000   21
# 2     3. John Tavares  TOR  $15,900,000   28
```

Powered by gazpacho:

```python
from gazpacho import get, Soup
import pandas as pd

url = 'https://www.capfriendly.com/browse/active/2020/salary?p=1'
response = get(url)
soup = Soup(response)
df = pd.read_html(str(soup.find('table')))[0]
print(df[['PLAYER', 'TEAM', 'SALARY', 'AGE']].head(3))

#                PLAYER TEAM       SALARY  AGE
# 0  1. Mitchell Marner  TOR  $16,000,000   22
# 1  2. Auston Matthews  TOR  $15,900,000   21
# 2     3. John Tavares  TOR  $15,900,000   28
```



#### Speed

gazpacho is fast:

```python
from gazpacho import Soup

%%timeit
soup = Soup(html)
soup.find('span', {'class': 'mw-headline'})
# 15 ms ± 325 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

gazpacho is often 20-40% faster than BeautifulSoup:

```python
from bs4 import BeautifulSoup

%%timeit
soup = BeautifulSoup(html, 'lxml')
soup.find('span', {'class': 'mw-headline'})
# 19.4 ms ± 583 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

And 200-300% faster than requests-html:

```python
from requests_html import HTML

%%timeit
soup = HTML(html=html)
soup.find('span.mw-headline')
# 40.1 ms ± 418 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```



#### Installation

```
pip install -U gazpacho
```



#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues).

For PRs, please read the [CONTRIBUTING.md](https://github.com/maxhumber/gazpacho/blob/master/README.md) file.