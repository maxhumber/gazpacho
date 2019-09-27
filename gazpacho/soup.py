from html.parser import HTMLParser

try:
    from .utils import match, html_starttag_and_attrs
except ModuleNotFoundError:
    from gazpacho.utils import match, html_starttag_and_attrs

class Soup(HTMLParser):
    '''HTML Parser Class

    - html (str): Full HTML text
    - tag (str, None): Found tag
    - attrs (dict, None): Found attributes
    - text (str, None): Found text
    - find (method): The main method to find HTML tags

    Examples:

    ```
    html = "<div><p id='foo'>bar</p><p id='foo'>baz</p><p id='zoo'>Tiger</p></div>"
    soup = Soup(html)
    result = soup.find('p', {'id': 'foo'})
    print(result)
    # [<p id="foo">bar</p>, <p id="foo">baz</p>]
    result = soup.find('p', {'id': 'zoo'})
    print(result)
    # <p id="zoo">Tiger</p>
    print(result.text)
    # Tiger
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
        '''Find a tag with optional attributes

        - tag (str): HTML tag to find
        - attrs (dict, optional): Attributes within tag to match
        '''
        self.tag = tag
        self.attrs = attrs
        self.count = 0
        self.group = 0
        self.groups = []
        super().feed(self.html)
        if len(self.groups) == 1:
            return self.groups[0]
        return self.groups
