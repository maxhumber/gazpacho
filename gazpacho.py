from copy import copy
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

def match(query_attrs, attrs):
    '''Match a query dictionary to an attrs dictionary'''
    if not query_attrs:
        return True
    if not query_attrs and not attrs:
        return True
    if query_attrs and not attrs:
        return False
    bools = []
    for k, v in query_attrs.items():
        if not attrs.get(k):
            bools.append(False)
        elif v in attrs.get(k):
            bools.append(True)
        else:
            bools.append(False)
    return all(bools)

def html_starttag_and_attrs(tag, attrs, startendtag=False):
    '''Reconstruct starttag and convert attrs to a dictionary'''
    if attrs:
        attrs = dict(attrs)
        af = [f'{k}="{v}"' for k, v in attrs.items()]
        af = f' {" ".join(af)}'
    else:
        attrs = {}
        af = ''
    if startendtag:
        html = f'<{tag}{af} />'
    else:
        html = f'<{tag}{af}>'
    return html, attrs

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.tag = None
        self.attrs = None
        self.data = None

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        # activate recording
        if tag == self.tag and match(self.attrs, attrs):
            self.count += 1
            self.group += 1
            self.groups.append(Soup(''))
            self.groups[self.group - 1].html += html
            self.groups[self.group - 1].tag = tag
            self.groups[self.group - 1].attrs = attrs
            return
        if self.count:
            self.count += 1
            self.groups[self.group - 1].html += html
            return
        else:
            return

    def handle_startendtag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs, True)
        if self.count:
            self.groups[self.group - 1].html += html
            return
        else:
            return

    # TODO: set data attribute
    def handle_data(self, data):
        if self.count:
            self.groups[self.group - 1].html += data
            return
        else:
            return

    def handle_endtag(self, tag):
        if self.count:
            end_tag = f'</{tag}>'
            self.groups[self.group - 1].html += end_tag
            self.count -= 1
            return
        else:
            return

    def find(self, tag, attrs=None):
        '''Find a tag with optional attributes'''
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.group = 0
        self.groups = []
        super().feed(self.html)
        return self.groups

# TODO:
# attribute setting? maybe not...
# hide methods from HTMLParser
# fix indenting (pretty print html)
