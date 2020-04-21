from gazpacho import get

url = 'https://en.wikipedia.org/wiki/Gazpacho'
html = get(url)
print(html[:50])

url = 'https://httpbin.org/anything'
get(url, params={'foo': 'bar', 'bar': 'baz'}, headers={'User-Agent': 'gazpacho'})

from gazpacho import Soup

soup = Soup(html)
str(soup)[:50]

# '<!DOCTYPE html>\n<html class="client-nojs" lang="en'

results = soup.find('span', {'class': 'mw-headline'})
results


soup.find('span', {'class': 'mw-headline'}, mode='first')


result = results[3]
print(result.html)
# <span class="mw-headline" id="In_Spain">In Spain</span>
print(result.tag)
# span
print(result.attrs)
# {'class': 'mw-headline', 'id': 'In_Spain'}
print(result.text)


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

from bs4 import BeautifulSoup

%%timeit
soup = BeautifulSoup(html, 'lxml')
soup.find('span', {'class': 'mw-headline'})

from requests_html import HTML

%%timeit
soup = HTML(html=html)
soup.find('span.mw-headline')
