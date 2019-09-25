from copy import copy
from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'

METHODS_TO_HIDE = set(dir(HTMLParser()))

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
    '''Match a query dictionary to a reference dictionary'''
    if not dict_query:
        return True
    if not dict_query and not dict_to_match:
        return True
    if dict_query and not dict_to_match:
        return False
    bools = []
    for k, v in dict_query.items():
        if not dict_to_match.get(k):
            bools.append(False)
        elif v in dict_to_match.get(k):
            bools.append(True)
        else:
            bools.append(False)
    return all(bools)

######## working here

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html

    def __repr__(self):
        return self.html

    @staticmethod
    def html_and_attrs(tag, attrs, startendtag=False):
        if attrs:
            attrs = dict(attrs)
            a = [f'{k}="{v}"' for k, v in attrs.items()]
            attrs_formatted = f' {" ".join(a)}'
        else:
            attrs = None
            attrs_formatted = ''
        if startendtag:
            html = f'<{tag}{attrs_formatted} />'
        else:
            html = f'<{tag}{attrs_formatted}>'
        return html, attrs

    def handle_starttag(self, tag, attrs):
        html, attrs = self.html_and_attrs(tag, attrs)
        if self.tag == tag and match(self.attrs, attrs) and not self.count:
            self.count += 1
            self.tag_ = tag
            self.attrs_ = attrs
            self.html_ += html
            return
        if self.tag == tag:
            self.count += 1
        if not self.count:
            self.html_ += ' '
            return
        self.html_ += html

    # BUG: not working
    def handle_startendtag(self, tag, attrs):
        if not self.tag_:
            return
        html, attrs = self.html_and_attrs(tag, attrs, True)
        self.html_ += html

    def handle_data(self, data):
        if not self.tag_:
            return
        self.html_ += data

    def handle_endtag(self, tag):
        print(tag, self.count)
        if not self.tag_:
            return
        self.html_ += f'</{tag}>'
        self.count -= 1

    def find(self, tag, attrs=None):
        '''Find a tag with optional attributes'''
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.tag_ = None
        self.attrs_ = None
        self.data_ = None
        self.html_ = ''
        super().feed(self.html)
        soup = Soup(self.html_)
        del self.html_
        return soup

{'class': 'foo', 'id': 'bar'}
html = '''
<div class="foo" id="bar">
  <p>'IDK!'</p>
  <br/>
  <div class='baz'>
    <div>
      <span>Hi</span>
    </div>
  </div>
</div>'''

soup = Soup(html)
soup.find('div', {'class': 'baz'})
# unindent
print(str(soup2))
soup.tag_
soup.attrs_
soup.dat

soup.recording
print(soup.html)
print(soup2.html)


######


class SoupBad(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.capture = False

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
            html = self.format(self.capture_tag, self.capture_attrs, data)
            soup = Soup(html)
            if self.capture_attrs:
                for k, v in self.capture_attrs.items():
                    if k == 'class':
                        k = 'class_'
                    setattr(soup, k, v)
            soup.attrs = copy(self.capture_attrs)
            soup.data = copy(data)
            self.data.append(soup)

    def find(self, tag, attrs=None):
        '''Find a tag with optional attributes'''
        self.tag = tag
        self.attrs = attrs
        self.data = []
        super().feed(self.html)
        return self.data

# TODO:
# hide methods
