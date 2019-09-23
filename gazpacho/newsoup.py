from html.parser import HTMLParser
import re
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# params = '?' + urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#
# url = "http://www.musi-cal.com/cgi-bin/query?{params}"
# with urllib.request.urlopen(url) as f:
#     print(f.read().decode('utf-8'))

def get(url):
    with urlopen(url) as f:
        html = f.read().decode('utf-8')
    return html

def match(dict_query, dict_to_match):
    if dict_query is None:
        return True
    for k, v in dict_query.items():
        if dict_to_match.get(k) != v:
            return False
    return True

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.capture = False

    def __repr__(self):
        return self.html

    def __str__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        if tag != self.tag:
            return
        if match(self.attrs, dict(attrs)):
            self.capture = True

    def handle_endtag(self, tag):
        if tag == self.tag:
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.data.append(data)

    def find(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs
        self.data = []
        super().feed(self.html)
        return self.data

url = 'https://www.goodreads.com/quotes/search?commit=Search&page=2&q=blake+crouch'
html = get(url)

soup = Soup(html)
results = soup.find('div', {'class': 'quoteText'})
Soup(results[0])




# hide bad methods
# return with original wrapping tags
# get href attributes, text attributes,
