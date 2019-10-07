try:
    from .utils import match, html_starttag_and_attrs
except ModuleNotFoundError:
    from gazpacho.utils import match, html_starttag_and_attrs

from gazpacho import get

url = 'https://en.wikipedia.org/wiki/Gazpacho'
html = get(url)
print(html[:50])

# <!DOCTYPE html>
# <html class="client-nojs" lang="en

url = 'https://httpbin.org/anything'
get(url, params={'foo': 'bar', 'bar': 'baz'}, headers={'User-Agent': 'gazpacho'})

from gazpacho import Soup

soup = Soup(html)
str(soup)[:50]

# '<!DOCTYPE html>\n<html class="client-nojs" lang="en'

# Original HTML: <span class="mw-headline" id="Ingredients_and_preparation">Ingredients and preparation</span>

results = soup.find('span', {'class': 'mw-headline'})

len(results)

soup.find('span', {'class': 'mw-headline'}, mode='first')

from gazpacho import get, Soup
import pandas as pd

url = 'https://www.capfriendly.com/browse/active/2020/salary?p=1'
response = get(url)
soup = Soup(response)
df = pd.read_html(str(soup.find('table')))[0]
print(df[['PLAYER', 'TEAM', 'SALARY', 'AGE']].head(3))

from gazpacho import Soup

%%timeit
soup = Soup(html)
soup.find('span', {'class': 'mw-headline'})
# 15 ms ± 325 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)




#
