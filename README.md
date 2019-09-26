<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/images/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-zero-blueviolet"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="Downloads" src="https://img.shields.io/pypi/dm/gazpacho.svg"></a>
</p>



#### About

gazpacho is a pure python web scraping library. 

It replaces requests and BeautifulSoup for most projects, but not all projects.

gazpacho is small, simple, and predictable.



#### Usage

To use gazpacho you need two things: `get` and `.find`. 

Here's a quick example:

```python
from gazpacho import get, Soup

url = 'https://en.wikipedia.org/wiki/Gazpacho'
html = get(url)
soup = Soup(html)
soup.find('span', {'class': 'mw-headline'})

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



#### Installation

```
pip install gazpacho
```



#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/gazpacho/issues)
