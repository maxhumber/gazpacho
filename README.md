<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/gazpacho.png" width="200px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="MIT" src="https://img.shields.io/github/license/maxhumber/gazpacho.svg"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="Downloads" src="https://img.shields.io/pypi/dm/gazpacho.svg"></a>
</p>

#### About

gazpacho is not BeautifulSoup.



#### Usage

gazpacho is easy to use.

```python
from gazpacho import Soup, get

html = get('www.google.com')
soup = Soup(html)
soup.find('a')
```



#### Installation

```
pip install gazpacho
```



#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues)
