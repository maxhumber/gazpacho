from copy import copy
from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener
from collections import Counter

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.counter = Counter()
        self.html_ = ''

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        if attrs:
            attrs = dict(attrs)
            a = [f'{k}="{v}"' for k, v in attrs.items()]
            attrs_formatted = f' {" ".join(a)}'
        else:
            attrs_formatted = ''
        self.tag = tag
        self.attrs = attrs
        html_ = f'<{tag}{attrs_formatted}>'
        self.html_ += html_
        self.counter.update([tag])

    def handle_data(self, data):
        self.html_ += data

    def handle_endtag(self, tag):
        self.counter[tag] -= 1
        self.html_ += f'</{tag}>'

    def stream(self):
        '''Find a tag with optional attributes'''
        super().feed(self.html)

{'class': 'foo', 'id': 'bar'}
html = '''<div class="foo" id="bar">
  <div class='baz'>
    Hi
  </div>
</div>'''

soup = Soup(html)
soup.stream()
print(soup.html_)
