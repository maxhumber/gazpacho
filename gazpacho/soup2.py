from collections import Counter
from html.parser import HTMLParser

from gazpacho.utils import match, html_starttag_and_attrs

debug = False

class Soup2(HTMLParser):

    @staticmethod
    def void(tag):
        return tag in ["img", "link"]

    @property
    def recording(self):
        return sum(self.counter.values()) > 0

    def __repr__(self):
        return self.html

    def __init__(self, html=None):
        super().__init__()
        self.html = "" if not html else html
        self.tag = None
        self.attrs = None
        self.text = None

    def handle_start(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(self.attrs, attrs)

        # if match and not already recording
        if (tag == self.tag) and (matching) and (not self.recording):
            self.groups.append(Soup2())
            self.groups[-1].tag = tag
            self.groups[-1].attrs = attrs
            self.groups[-1].html += html
            self.counter[tag] += 1
            # print(sum(self.counter.values()))
            return

        # if already recording
        if self.recording:
            self.groups[-1].html += html
            self.counter[tag] += 1

        if debug:
            print(f'{tag} (start) +1 = {self.counter[tag]}')

    def handle_starttag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.recording:
            if self.void(tag):
                self.counter[tag] -= 1

        if debug:
            print(f'{tag} (void)  -1 = {self.counter[tag]}')

    def handle_startendtag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.recording:
            self.counter[tag] -= 1

        if debug:
            print(f'{tag} (s/end) -1 = {self.counter[tag]}')

    def handle_data(self, data):
        if self.recording:
            if self.groups[-1].text is None:
                self.groups[-1].text = data.strip()
            self.groups[-1].html += data

    def handle_endtag(self, tag):
        if self.recording:
            self.groups[-1].html += f"</{tag}>"
            self.counter[tag] -= 1

        if debug:
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
    <div id="hi2">Gotcha</div>
</div>
"""

soup = Soup2(html)
results = soup.find('div', {'id': 'hi2'})

soup.find('img')[2]

results

#
