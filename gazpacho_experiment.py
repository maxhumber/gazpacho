from copy import copy
from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener
from collections import Counter

def html_and_attrs(tag, attrs, startendtag=False):
    if attrs:
        attrs = dict(attrs)
        a = [f'{k}="{v}"' for k, v in attrs.items()]
        attrs_formatted = f' {" ".join(a)}'
    else:
        attrs_formatted = ''
    if startendtag:
        html = f'<{tag}{attrs_formatted} />'
    else:
        html = f'<{tag}{attrs_formatted}>'
    return html, attrs

class Soup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.counter = Counter()

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        self.counter.update([tag])
        html, attrs = html_and_attrs(tag, attrs)
        self.capture_tag = tag
        self.capture_attrs = attrs
        self.html += html

    def handle_startendtag(self, tag, attrs):
        html, attrs = html_and_attrs(tag, attrs, True)
        self.html += html

    def handle_data(self, data):
        self.html += data

    def handle_endtag(self, tag):
        self.counter[tag] -= 1
        self.html += f'</{tag}>'

    def find(self, tag):
        '''Find a tag with optional attributes'''
        self.tag = tag
        html_ = copy(self.html)
        self.html = ''
        super().feed(html_)

{'class': 'foo', 'id': 'bar'}
html = '''
<div class="foo" id="bar">
  <p>'IDK!'</p>
  <br/>
  <div class='baz'>
    <div>
      <span>Hi</span>
    <div>
  </div>
</div>'''

soup = Soup(html)
soup.find('div')
soup.counter
print(soup.html)






###
