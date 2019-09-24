from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener

def get(url, params=None, headers=None):
    if params:
        url += '?' + urlencode(params)
    if not headers:
        with urlopen(url) as f:
            html = f.read().decode('utf-8')
    else:
        opener = build_opener()
        for h in headers.items():
            opener.addheaders = [h]
        with opener.open(url) as f:
            html = f.read().decode('utf-8')
    return html

# TODO:
# FIX PARTIAL MATCH
dict_to_match = {'class': "teamName teamId-1"}
dict_query = {'class': 'teamName'}
match(dict_query, dict_to_match)

def match(dict_query, dict_to_match):
    if dict_query is None:
        return True
    for k, v in dict_query.items():
        if dict_to_match.get(k) != v:
            return False
    return True

# Figure out how to make a unified interface
class SoupCan:
    def __init__(self, tag, attrs=None, data=None):
        self.tag = tag
        self.attrs = attrs
        self.data = data
        self.html = format(self.tag, self.attrs, self.data)
        if attrs:
            for k, v in attrs.items():
                if k == 'class':
                    k = 'class_'
                setattr(self, k, v)

    def __str__(self):
        return self.html

    def __repr__(self):
        return self.html

    @staticmethod
    def format(tag, attrs, data):
        if not data:
            data = ''
        if attrs:
            attrs = [f'{k}="{v}"' for k, v in attrs.items()]
            attrs = f' {" ".join(attrs)}'
        else:
            attrs = ''
        return f'<{tag}{attrs}>{data}</{tag}>'

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.capture = False

    def handle_starttag(self, tag, attrs):
        if tag != self.tag:
            return
        if match(self.attrs, dict(attrs)):
            self.capture = True
            self.capture_tag = tag
            self.capture_attrs = dict(attrs)

    def handle_endtag(self, tag):
        if tag == self.tag:
            self.capture = False
            self.capture_tag = None
            self.capture_attrs = None

    def handle_data(self, data):
        if self.capture:
            data = SoupCan(self.capture_tag, self.capture_attrs, data)
            self.data.append(data)

    def find(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs
        self.data = []
        super().feed(self.html)
        return self.data

url = 'https://en.wikipedia.org/wiki/Fantasy_hockey'
html = get(url)
soup = Soup(html)

results = soup.find('span', {'class': 'mw-headline'})
results[0]

url = 'https://www.goodreads.com/quotes/search'
params = {'commit': 'Search', 'page': 2, 'q': 'blake crouch'}
html = get(url, params)

soup = Soup(html)
soup.find('a')

@staticmethod
def format_html(tag, attrs, data):
    attrs = [f'{k}="{v}"' for k, v in attrs.items()]
    return f'<{tag} {" ".join(attrs)}>{data}</{tag}>'

tag = 'a'
attrs = {'href': '/genres', 'class': 'siteHeader__subNavLink siteHeader__subNavLink--genresIndex', 'data-reactid': '.1638wh2cfls.1.0.3.0.2.0.1.0.0.2.0'}

attrs = [f'{k}="{v}"' for k, v in attrs.items()]

content = 'hi'
f'<{tag} {" ".join(attrs)}>{content}</{tag}>'



results = soup.find('div', {'class': 'quoteText'})
results

# add all attrs to the data container? could be handy
# hide bad methods
# return with original wrapping tags
# get href attributes, text attributes,
