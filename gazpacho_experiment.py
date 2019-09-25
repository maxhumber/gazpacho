from copy import copy
from html.parser import HTMLParser
import re
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener

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
        self.recording = 0

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        if self.tag == tag:
            self.recording += 1
        if not self.recording:
            return
        html, attrs = html_and_attrs(tag, attrs)
        self.capture_tag = tag
        self.capture_attrs = attrs
        self.html_ += html

    def handle_startendtag(self, tag, attrs):
        if not self.recording:
            return
        html, attrs = html_and_attrs(tag, attrs, True)
        self.html_ += html

    def handle_data(self, data):
        if not self.recording:
            return
        self.html_ += data

    def handle_endtag(self, tag):
        if not self.recording:
            return
        self.recording -= 1
        self.html_ += f'</{tag}>'

    def find(self, tag):
        '''Find a tag with optional attributes'''
        self.tag = tag
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
    <div>
  </div>
</div>'''

soup = Soup(html)
soup2 = soup.find('p')
soup2
soup.recording
print(soup.html)
print(soup2.html)






###
