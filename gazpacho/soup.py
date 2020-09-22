from collections import Counter
from html.parser import HTMLParser
import re

from .utils import match, html_starttag_and_attrs
from .get import get


class Soup(HTMLParser):
    """HTML Soup Parser

    Attributes:

    - html (str): HTML content to parse
    - tag (str, None): HTML element tag returned by find
    - attrs (dict, None): HTML element attributes returned by find
    - text (str, None): HTML element text returned by find

    Methods:

    - find: return matching HTML elements {'auto', 'all', 'first'}

    Examples:

    ```
    from gazpacho import Soup

    html = "<div><p id='foo'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
    soup = Soup(html)

    soup.find('p', {'id': 'foo'})
    # [<p id="foo">bar</p>, <p id="foo">baz</p>]

    result = soup.find('p', {'id': 'foo'}, mode='first')
    print(result)
    # <p id="foo">bar</p>

    result = soup.find('p', {'id': 'zoo'}, mode='auto')
    print(result)
    # <p id="zoo">bat</p>

    print(result.text)
    # bat
    ```
    """

    def __init__(self, html=None):
        """Params:

        - html (str): HTML content to parse
        """
        super().__init__()
        self.html = "" if not html else html
        self.tag = None
        self.attrs = None
        self.text = None

    def __dir__(self):
        # what to expose here?
        return ["html", "tag", "attrs", "text", "find"]

    def __repr__(self):
        return self.html

    # EXPERIMENTAL is this the right way?
    # Soup.get(), Soup.post()
    # Soup.from_url(method="GET/POST")
    # Soup.read_url(method="GET/POST") like pandas
    # Soup("www.example.com")
    # Soup.url()
    # import gazpacho as gz; gz.from_url; gz.Soup()
    @classmethod
    def get(cls, url, params=None, headers=None):
        html = get(url, params, headers)
        soup = Soup(html)
        return soup

    # is recording the right word?
    @property
    def recording(self):
        return sum(self.counter.values()) > 0

    @staticmethod
    def void(tag):
        return tag in [
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "keygen",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        ]

    def handle_start(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(self.attrs, attrs, partial=self.partial)

        # if match and not already recording
        if (tag == self.tag) and (matching) and (not self.recording):
            self.groups.append(Soup())
            self.groups[-1].tag = tag
            self.groups[-1].attrs = attrs
            self.groups[-1].html += html
            self.counter[tag] += 1
            return

        # if already recording
        if self.recording:
            self.groups[-1].html += html
            self.counter[tag] += 1

    def handle_starttag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.recording:
            if self.void(tag):
                self.counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.recording:
            self.counter[tag] -= 1

    def handle_data(self, data):
        if self.recording:
            if self.groups[-1].text is None:
                self.groups[-1].text = data.strip()
            self.groups[-1].html += data

    def handle_endtag(self, tag):
        if self.recording:
            self.groups[-1].html += f"</{tag}>"
            self.counter[tag] -= 1

    def remove_tags(self, strip=True):
        """Remove all HTML element tags

        Params:

        - strip (bool, True): Strip all extra whitespace

        Example:

        ```
        html = '<span>Hi! I like <b>soup</b>.</span>'
        soup = Soup(html)
        soup.remove_tags()

        # Hi! I like soup.
        ```
        """
        text = re.sub("<[^>]+>", "", self.html)
        if strip:
            text = " ".join(text.split())
        return text

    # need a strict deprecation message here
    def find(self, tag, attrs=None, *, mode="auto", partial=True):
        """Return matching HTML elements

        Params:

        - tag (str): HTML element tag to find
        - attrs (dict, optional): HTML element attributes to match
        - mode (str, 'auto'): Element(s) to return {'auto', 'all', 'first'}
        - strict (bool, False): Require exact attribute matching

        Examples:

        ```
        html = "<div><p id='foo foo-striped'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
        soup = Soup(html)

        soup.find('p')
        # [<p id="foo foo-striped">bar</p>, <p id="foo">baz</p>, <p id="zoo">bat</p>]

        soup.find('p', {'id': 'foo'})
        # [<p id="foo foo-striped">bar</p>, <p id="foo">baz</p>]

        result = soup.find('p', {'id': 'foo'}, mode='first')
        print(result)
        # <p id="foo">bar</p>

        soup.find('p', {'id': 'foo'}, partial=False)
        # [<p id="foo">baz</p>]
        ```
        """
        self.tag = tag
        self.attrs = attrs
        self.partial = partial
        self.counter = Counter()
        self.groups = []
        self.feed(self.html)

        # does this make it more confusing? Undecided
        # first
        modeX = ["first", "head"] # leave off head

        # last
        modeX = ["last", "tail"]

        # random
        modeX = ["one", "random", "sample"]

        # all
        modeX = ["all", "list"]

        # automatic
        modeX = ["auto", "automatic"] # could probably make this no problem

        # if wrong mode, raise error

        if mode in ["auto", "first"] and not self.groups:
            return None
        if mode == "all":
            return self.groups
        if mode == "first":
            return self.groups[0]
        if mode == "auto":
            if len(self.groups) == 1:
                return self.groups[0]
            return self.groups
