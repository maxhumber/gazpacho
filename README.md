<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/images/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
	<a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/gazpacho.svg"></a>
  <a href="https://pepy.tech/project/gazpacho"><img alt="Downloads" src="https://pepy.tech/badge/gazpacho"></a>  
</p>




## About

gazpacho is a simple, fast, and modern web scraping library. The library is stable, actively maintained, and installed with **zero** dependencies.



## Install

Install with `pip` at the command line:

```
pip install -U gazpacho
```



## Quickstart

Give this a try:

```python
from gazpacho import get, Soup

url = 'https://scrape.world/books'
html = get(url)
soup = Soup(html)
books = soup.find('div', {'class': 'book-'}, partial=True)

def parse(book):
    name = book.find('h4').text
    price = float(book.find('p').text[1:].split(' ')[0])
    return name, price

[parse(book) for book in books]
```



## Tutorial

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

Adjust `get` requests with optional params and headers:

```python
get(
    url='https://httpbin.org/anything',
    params={'foo': 'bar', 'bar': 'baz'},
    headers={'User-Agent': 'gazpacho'}
)
```



#### Soup

Use the `Soup` wrapper on raw html to enable parsing:

```python
soup = Soup(html)
```

Soup objects can alternatively be initialized with the  `.get` classmethod:

```python
soup = Soup.get(url)
```



#### .find

Use the `.find` method to target and extract HTML tags:

```python
h1 = soup.find('h1')
print(h1)
# <h1 id="firstHeading" class="firstHeading" lang="en">Soup</h1>
```



#### attrs=

Use the `attrs` argument to isolate tags that contain specific HTML element attributes:

```python
soup.find('div', attrs={'class': 'section-'})
```



#### partial=

Element attributes are partially matched by default. Turn this off by setting `partial` to `False`:  

```python
soup.find('div', {'class': 'soup'}, partial=False)
```



#### mode=

Override the mode argument {`'auto', 'first', 'all'`} to guarantee return behaviour:

```python
print(soup.find('span', mode='first'))
# <span class="navbar-toggler-icon"></span>
len(soup.find('span', mode='all'))
# 8
```



#### dir()

`Soup` objects have `html`, `tag`, `attrs`, and `text` attributes:

```python
dir(h1)
# ['attrs', 'find', 'get', 'html', 'strip', 'tag', 'text']
```

Use them accordingly:

```python
print(h1.html)
# '<h1 id="firstHeading" class="firstHeading" lang="en">Soup</h1>'
print(h1.tag)
# h1
print(h1.attrs)
# {'id': 'firstHeading', 'class': 'firstHeading', 'lang': 'en'}
print(h1.text)
# Soup
```



## Support

If you use gazpacho, consider adding the [![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho) badge to your project README.md:

```markdown
[![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho)
```



## Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues)

For PRs, please read the [CONTRIBUTING.md](https://github.com/maxhumber/gazpacho/blob/master/CONTRIBUTING.md) document
