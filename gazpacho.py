from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'

def get(url, params=None, headers=None):
    '''Get the content from a URL

    url: The URL for the webpage
    params: A dictionary of the param payload
    headers: A dictionary for the headers to be added

    Example:
    get('https://httpbin.org/anything', {'soup': 'gazpacho'})
    '''
    opener = build_opener()
    if params:
        url += '?' + urlencode(params)
    if headers:
        for h in headers.items():
            opener.addheaders = [h]
    else:
        opener.addheaders = [('User-Agent', DEFAULT_USER_AGENT)]
    with opener.open(url) as f:
        content = f.read().decode('utf-8')
    return content

def match(dict_query, dict_to_match):
    '''Match a query to a reference dictionary'''
    if dict_query is None:
        return True
    bools = []
    for k, v in dict_query.items():
        if not dict_to_match.get(k):
            bools.append(False)
        elif v in dict_to_match.get(k):
            bools.append(True)
        else:
            bools.append(False)
    return all(bools)

class SoupCan:
    def __init__(self, tag, attrs=None, data=None):
        self.tag = tag
        self.attrs = attrs
        self.data = data
        self.html = self.format(self.tag, self.attrs, self.data)
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

if __name__ == '__main__':

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

    results = soup.find('div', {'class': 'quoteText'})
    results

    # add all attrs to the data container? could be handy
    # hide bad methods
    # return with original wrapping tags
    # get href attributes, text attributes,
