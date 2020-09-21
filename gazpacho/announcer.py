from html.parser import HTMLParser
from html.entities import name2codepoint
from collections import Counter

from gazpacho.utils import match, html_starttag_and_attrs

class MyHTMLParser(HTMLParser):

    @staticmethod
    def is_void_tag(tag):
        return tag in ["img", "link"]

    def __init__(self, html=None, debug=True):
        super().__init__()
        if html:
            self.html = html
        self.debug = debug
        self.counter = Counter()
        self.recording = False

    def handle_starttag(self, tag, attrs):
        self.counter[tag] += 1
        if self.debug:
            print("Start tag:", tag)
            for attr in attrs:
                print("     attr:", attr)
        if self.is_void_tag(tag):
            self.counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self.counter[tag] += 1
        if self.debug:
            print("Start tag:", tag)
            for attr in attrs:
                print("     attr:", attr)
        self.counter[tag] -= 1

    def handle_endtag(self, tag):
        if self.debug:
            print("End tag  :", tag)
        self.counter[tag] -= 1

    def find(self, tag):
        self.tag = tag
        self.chunks = []
        self.feed(self.html)

with open("sand.html", "r") as f:
    html = f.read()

# one
parser = MyHTMLParser()
parser.feed(html)
parser.counter


# two
parser = MyHTMLParser(html, debug=False)
parser.find('link')
parser.counter




print(html)
