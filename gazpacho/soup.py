from html.parser import HTMLParser
from .utils import match, html_starttag_and_attrs

class Soup(HTMLParser):
    '''HTML Soup Parser

    Attributes:

    - html (str): HTML content to parse
    - tag (str, None): HTML element tag returned by find
    - attrs (dict, None): HTML element attributes returned by find
    - text (str, None): HTML element text returned by find

    Methods:

    - find: return all matching HTML elements
    - find_one: return the first matching HTML element

    Examples:

    ```
    from gazpacho import Soup

    html = "<div><p id='foo'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
    soup = Soup(html)

    soup.find('p', {'id': 'foo'})
    # [<p id="foo">bar</p>, <p id="foo">baz</p>]

    result = soup.find_one('p', {'id': 'zoo'})
    print(result)
    # <p id="zoo">bat</p>

    print(result.text)
    # bat
    ```
    '''

    def __init__(self, html):
        '''Params:

        - html (str): HTML content to parse
        '''
        super().__init__()
        self.html = html
        self.tag = None
        self.attrs = None
        self.text = None

    def __dir__(self):
        return ['html', 'tag', 'attrs', 'text', 'find', 'find_one']

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(self.attrs, attrs, self.strict)
        if tag == self.tag and matching and not self.count:
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

    def handle_data(self, data):
        if self.count:
            if self.groups[self.group - 1].text is None:
                self.groups[self.group - 1].text = data.strip()
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

    def find(self, tag, attrs=None, strict=False):
        '''Return all matching HTML elements

        Params:

        - tag (str): HTML element tag to find
        - attrs (dict, optional): HTML element attributes to match
        - strict (bool, False): Require exact attribute matching

        Examples:

        ```
        html = "<div><p id='foo foo-striped'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
        soup = Soup(html)

        soup.find('p')
        # [<p id="foo foo-striped">bar</p>, <p id="foo">baz</p>, <p id="zoo">bat</p>]

        soup.find('p', {'id': 'foo'})
        # [<p id="foo foo-striped">bar</p>, <p id="foo">baz</p>]

        soup.find('p', {'id': 'foo'}, strict=True)
        # [<p id="foo">baz</p>]
        ```
        '''
        self.tag = tag
        self.attrs = attrs
        self.strict = strict
        self.count = 0
        self.group = 0
        self.groups = []
        self.feed(self.html)
        soups = self.groups
        return soups

    def find_one(self, tag, attrs=None, strict=False):
        '''Return the first matching HTML element

        Params:

        - tag (str): HTML element tag to find
        - attrs (dict, optional): HTML element attributes to match
        - strict (bool, False): Require exact attribute matching

        Example (*for more see* `find`):

        ```
        html = "<div><p id='foo foo-striped'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
        soup = Soup(html)

        soup.find_one('p', {'id': 'foo'})
        # <p id="foo foo-striped">bar</p>
        '''
        self.tag = tag
        self.attrs = attrs
        self.strict = strict
        self.count = 0
        self.group = 0
        self.groups = []
        self.feed(self.html)
        soup = self.groups[0]
        return soup
