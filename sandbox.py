# Quickstart

from gazpacho import get, Soup

url = 'https://scrape.world/books'
html = get(url)
soup = Soup(html)
books = soup.find('div', {'class': 'book-'}, strict=False)

def parse(book):
    name = book.find('h4').text
    price = float(book.find('p').text[1:].split(' ')[0])
    return name, price

[parse(book) for book in books]

# Import

from gazpacho import get, Soup

# get

url = 'https://scrape.world/soup'
html = get(url)
print(html[:50])
# '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <met'

# optional

get(
    url='https://httpbin.org/anything',
    params={'foo': 'bar', 'bar': 'baz'},
    headers={'User-Agent': 'gazpacho'}
)

# Soup

soup = Soup(html)


# .find

h1 = soup.find('h1')
print(h1)
# <h1 id="firstHeading" class="firstHeading" lang="en">Soup</h1>

# attrs=

soup.find('div', attrs={'class': 'section-soup'})

# strict=

soup.find('div', {'class': 'section-'}, strict=False)

# mode=

print(soup.find('span', mode='first'))
# <span class="navbar-toggler-icon"></span>
len(soup.find('span', mode='all'))
# 8

# dir()

dir(h1)

print(h1.html)
# '<h1 id="firstHeading" class="firstHeading" lang="en">Soup</h1>'
print(h1.tag)
# h1
print(h1.attrs)
# {'id': 'firstHeading', 'class': 'firstHeading', 'lang': 'en'}
print(h1.text)
# Soup

# Comparison

# gazpacho

from gazpacho import get, Soup

url = 'http://quotes.toscrape.com/'
html = get(url)
soup = Soup(html)
quotes = soup.find('div', {'class': 'quote'})

def parse(quote):
    return {
        'author': quote.find('small').text,
        'text': quote.find('span', {'class': 'text'}).text
    }

%%timeit
[parse(quote) for quote in quotes]


#### BeautifulSoup

import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com/'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html)
quotes = soup.find_all('div', class_='quote')

def parse(quote):
    return {
        'author': quote.find('small').text,
        'text': quote.find('span', class_= 'text').text
    }

[parse(quote) for quote in quotes]








#
