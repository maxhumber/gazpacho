from html.parser import HTMLParser
from .utils import match, html_starttag_and_attrs

class Soup(HTMLParser):
    '''HTML Parser Class

    - html (str): Full HTML text
    - tag (str, None): Found tag
    - attrs (dict, None): Found attributes
    - text (str, None): Found text
    - find (method): The main method to find HTML tags
    - find_one (method): find, but for just one result

    Examples:

    ```
    from gazpacho import Soup
    html = "<div><p id='foo'>bar</p><p id='foo'>baz</p><p id='zoo'>bat</p></div>"
    soup = Soup(html)
    result = soup.find('p', {'id': 'foo'})
    print(result)
    # [<p id="foo">bar</p>, <p id="foo">baz</p>]
    result = soup.find_one('p', {'id': 'zoo'})
    print(result)
    # <p id="zoo">bat</p>
    print(result.text)
    # bat
    ```
    '''
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.tag = None
        self.attrs = None
        self.text = None

    def __dir__(self):
        return ['html', 'tag', 'attrs', 'text', 'find']

    def __repr__(self):
        return self.html

    def handle_starttag(self, tag, attrs):
        html, attrs = html_starttag_and_attrs(tag, attrs)
        if tag == self.tag and match(self.attrs, attrs) and not self.count:
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

    def find(self, tag, attrs=None):
        '''Find all HTML elements that match a tag and optional attributes

        - tag (str): HTML tag to find
        - attrs (dict, optional): Attributes within tag to match
        '''
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.group = 0
        self.groups = []
        super().feed(self.html)
        return self.groups

    def find_one(self, tag, attrs=None):
        '''Find one HTML element that matches a tag and optional attributes

        - tag (str): HTML tag to find
        - attrs (dict, optional): Attributes within tag to match
        '''
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.group = 0
        self.groups = []
        super().feed(self.html)
        soup = self.groups[0]
        return soup
