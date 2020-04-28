<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/images/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/"><img alt="Dependencies" src="https://img.shields.io/badge/scraper-gazpacho-C6422C"></a>
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-0-brightgreen"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pepy.tech/project/gazpacho"><img alt="Downloads" src="https://pepy.tech/badge/gazpacho"></a>  
</p>



#### About

gazpacho is a simple, fast, and modern web scraping library. The library is actively maintained, stable, and installed with zero dependencies. 



#### Install

Install gazpacho at the command line:

```
pip install -U gazpacho
```



#### Import

Import gazpacho following the convention:

```python
from gazpacho import get, Soup
```



#### get

Use the `get` function to download raw HTML:

```python
url = 'https://scrape.world/soup'
html = get(url)
print(html[:50])
# '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <met'
```

Use optional params and headers to adjust `get` requests:

```python
url = 'https://httpbin.org/anything'
get(url, params={'foo': 'bar', 'bar': 'baz'}, headers={'User-Agent': 'gazpacho'})
```



#### Soup

Use the `Soup` wrapper to turn raw HTML strings into parseable objects:

```python
soup = Soup(html)
```



#### .find

Use the `.find` method to target and extract HTML tags elements and elements:

```python
result = soup.find('span', {'id': 'As_a_figure_of_speech'})
print(result)
# <span class="mw-headline" id="As_a_figure_of_speech">As a figure of speech</span>
```



#### mode

Use the mode argument {`'auto', 'first', 'all'`} to adjust the return behaviour of `.find`:

```python
print(soup.find('span', mode='first'))
# <span class="navbar-toggler-icon"></span>
len(soup.find('span', mode='all'))
# 8
```



#### Chain

Use method chaining to join consecutive `.find` calls together:

```python
soup.find('div', {'class': 'section-speech'}).find('a')[-2]
# <a href="https://en.wikipedia.org/wiki/Tag_soup" title="Tag soup">Tag soup</a>
```



#### text



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



#### BeautifulSoup

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
# 1     2. John Tavares  TOR  $15,900,000   28
# 2  3. Auston Matthews  TOR  $15,900,000   21
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
# 1     2. John Tavares  TOR  $15,900,000   28
# 2  3. Auston Matthews  TOR  $15,900,000   21
```

#### Scrapy



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



#### Support

If you use gazpacho, consider adding the [![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho) badge to your project README.md:

```markdown
[![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho)
```



#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues).

For PRs, please read the [CONTRIBUTING.md](https://github.com/maxhumber/gazpacho/blob/master/CONTRIBUTING.md) document.
