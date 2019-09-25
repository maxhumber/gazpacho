<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/gazpacho/master/gazpacho.png" height="300px" alt="gazpacho">
</h3>
<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="MIT" src="https://img.shields.io/github/license/maxhumber/gazpacho.svg"></a>
  <a href="https://travis-ci.org/maxhumber/gazpacho"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="PyPI" src="https://img.shields.io/pypi/v/gazpacho.svg"></a>
  <a href="https://pypi.python.org/pypi/gazpacho"><img alt="Downloads" src="https://img.shields.io/pypi/dm/gazpacho.svg"></a>
</p>

#### ⚠️ Warning 

 gazpacho is in Beta right now. Expect some things to change.



#### About

gazpacho is not BeautifulSoup. 

Though gazpacho *is* a web scraping library, it's not a full-service web scraping library. Really, gazpacho just does two things: `get` and `.find`.



#### Usage

gazpacho is easy to use:

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
