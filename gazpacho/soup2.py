from collections import Counter
from html.parser import HTMLParser

from gazpacho.utils import match, html_starttag_and_attrs

class Soup2(HTMLParser):

    @staticmethod
    def is_void_tag(tag):
        return tag in ["img", "link"]

    def __repr__(self):
        return self.html

    def __init__(self, html=None):
        super().__init__()
        self.html = "" if not html else html
        self.tag = None
        self.attrs = None
        self.text = None

    def handle_starts(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(attrs, self.attrs)
        self.counter[tag] += 1
        print(f'{tag} (start) +1 = {self.counter[tag]}')


    def handle_starttag(self, tag, attrs):
        self.handle_starts(tag, attrs)
        if self.is_void_tag(tag):
            self.counter[tag] -= 1
            print(f'{tag} (void)  -1 = {self.counter[tag]}')

    def handle_startendtag(self, tag, attrs):
        self.handle_starts(tag, attrs)
        self.counter[tag] -= 1
        print(f'{tag} (s/end) -1 = {self.counter[tag]}')

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        self.counter[tag] -= 1
        print(f'{tag} (end)   -1 = {self.counter[tag]}')

    def find(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs
        self.counter = Counter()
        self.groups = []
        self.feed(self.html)
        return self.groups

# two
html = """
<div>
    <div id="hi">
        <div>Text is text</div>
    </div>
    <img src="test1.png">
    <img src="test2.png">
    <img src="test3.png" />
    <div id="hi">Bye</div>
</div>
"""

soup = Soup2(html)
soup.find('div')
soup.counter
