from html.parser import HTMLParser
import re
from .utils import match, html_starttag_and_attrs


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

    def __init__(self, html):
        """Params:

        - html (str): HTML content to parse
        """
        super().__init__()
        self.html = html
        self.tag = None
        self.attrs = None
        self.text = None

    def __dir__(self):
        return ["html", "tag", "attrs", "text", "find"]

    def __repr__(self):
        return self.html

    @staticmethod
    def _empty_tag(tag):
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

    def handle_starttag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(self.attrs, attrs, self.strict)
        if tag == self.tag and matching and not self.count:
            self.count += 1
            self.group += 1
            self.groups.append(Soup(""))
            self.groups[self.group - 1].html += html
            self.groups[self.group - 1].tag = tag
            self.groups[self.group - 1].attrs = attrs
            return
        if self.count:
            if not self._empty_tag(tag):
                self.count += 1
            self.groups[self.group - 1].html += html
        return

    def handle_startendtag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs, True)
        if self.count:
            self.groups[self.group - 1].html += html
        return

    def handle_data(self, data):
        if self.count:
            if self.groups[self.group - 1].text is None:
                self.groups[self.group - 1].text = data.strip()
            self.groups[self.group - 1].html += data
        return

    def handle_endtag(self, tag):
        if self.count:
            end_tag = f"</{tag}>"
            self.groups[self.group - 1].html += end_tag
            self.count -= 1
        return

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

    def find(self, tag, attrs=None, mode="auto", strict=False):
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

        soup.find('p', {'id': 'foo'}, strict=True)
        # [<p id="foo">baz</p>]
        ```
        """
        self.tag = tag
        self.attrs = attrs
        self.strict = strict
        self.count = 0
        self.group = 0
        self.groups = []
        self.feed(self.html)
        if mode == "all":
            return self.groups
        if mode == "first":
            return self.groups[0]
        if mode == "auto":
            if len(self.groups) == 1:
                return self.groups[0]
            return self.groups
