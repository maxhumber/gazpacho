<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/images/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-zero-blueviolet"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pepy.tech/badge/gazpacho"><img alt="Downloads" src="https://pepy.tech/badge/gazpacho"></a>  
</p>



#### About

gazpacho is a web scraping library. It replaces requests and BeautifulSoup for most projects. gazpacho is small, simple, fast, and consistent. You should use it! 



#### Usage

gazpacho is easy to use. To retrieve the contents of a web page use `get`. And to parse the retrieved contents use `Soup`.



####get 

The `get` function retrieves content from a web page:

```python
from gazpacho import get, Soup

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

The `Soup` object takes an html string and turns it into something parsable:

```python
soup = Soup(html)
str(soup)[:50]

# '<!DOCTYPE html>\n<html class="client-nojs" lang="en'
```

In order to parse an html element in a `Soup` object, pass the tag and optional attributes to the `find` method:

```python
# Original HTML: <span class="mw-headline" id="Ingredients_and_preparation">Ingredients and preparation</span>

results = soup.find('span', {'class': 'mw-headline'})
```

The `find` method will return one `Soup` object if it finds exactly one element that satisfies the tag and attribute constraints, or a list of `Soup` objects if it finds more than one:

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

`Soup` objects returned by the `find` method will have `html`, `tag`, `attrs`, and `text` attributes:

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

Crucially, returned `Soup` objects can reimplement the `find` method!



#### Production

gazpacho is production ready. It currently powers another library, [quote](https://github.com/maxhumber/quote), a python wrapper for the Goodreads Quote API.



#### Comparison

gazpacho is a drop-in replacement for most projects that use requests and BeautifulSoup.

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

And powered by gazpacho:

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



#### Installation

```
pip install gazpacho
```



#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues)
