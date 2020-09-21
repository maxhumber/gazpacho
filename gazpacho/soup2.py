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
        matching = match(self.attrs, attrs)

        if tag == self.tag and matching and not self.counter[tag]:
            self.groups.append(Soup2())
            self.groups[-1].html += html
            self.groups[-1].tag = tag
            self.groups[-1].attrs = attrs
            self.counter[tag] += 1
        elif self.counter[tag]:

        self.groups[-1].html += html
        self.counter[tag] += 1

    def handle_starttag(self, tag, attrs):
        self.handle_starts(tag, attrs)
        if self.is_void_tag(tag):
            self.counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starts(tag, attrs)
        self.counter[tag] -= 1

    def handle_data(self, data):
        if self.counter[self.tag]:
            try:
                if self.groups[-1].text is None:
                    self.groups[-1].text = data.strip()
                self.groups[-1].html += data
            except IndexError:
                pass

    def handle_endtag(self, tag):
        if self.counter[tag]:
            self.groups[-1].html += f"</{tag}>"
        self.counter[tag] -= 1

    def find(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.groups = []
        self.feed(self.html)
        return self.groups

# with open("sand.html", "r") as f:
#     html = f.read()
#
# # one
# parser = Soup2()
# parser.feed(html)
# parser.counter

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

soup.find('div', {'id': 'hi'})

soup.find('img')


sum(soup.counter.values())

soup.groups





print(html)
