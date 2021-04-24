import re
import warnings
from collections import Counter
from html.parser import HTMLParser
from random import sample


class Parser(HTMLParser):
    def __init__(self, html=""):
        super().__init__()
        self._html = "" if not html else html
        self.tag = ""
        self.attrs = None
        self.text = ""

    @staticmethod
    def match(a, b, *, partial=False):
        if (not a) or (not a and not b):
            return True
        if a and (not b):
            return False
        for key, lhs in a.items():
            rhs = b.get(key)
            if not rhs:
                return False
            if not partial:
                if lhs == rhs:
                    continue
                return False
            if lhs in rhs:
                continue
            return False
        return True

    @staticmethod
    def recover_html_and_attrs(tag, attrs, startendtag=False):
        if attrs:
            attrs_dict = dict(attrs)
            attrs_list = [f'{key}="{value}"' for key, value in attrs_dict.items()]
            attrs_str = f' {" ".join(attrs_list)}'
        else:
            attrs_dict = {}
            attrs_str = ""
        if startendtag:
            html = f"<{tag}{attrs_str} />"
        else:
            html = f"<{tag}{attrs_str}>"
        return html, attrs_dict

    @staticmethod
    def is_void(tag):
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

    @property
    def is_active(self):
        return sum(self._counter.values()) > 0

    def handle_start(self, tag, attrs):
        html, attrs_dict = recover_html_and_attrs(tag, attrs)
        query_attrs = {} if not self.attrs else self.attrs
        matching = match(query_attrs, attrs_dict, partial=self._partial)

        if (tag == self.tag) and (matching) and (not self.is_active):
            self._groups.append(Soup())
            self._groups[-1].tag = tag
            self._groups[-1].attrs = attrs_dict
            self._groups[-1]._html += html
            self._counter[tag] += 1
            return

        if self.is_active:
            self._groups[-1]._html += html
            self._counter[tag] += 1

    def handle_starttag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.is_active:
            if self.is_void(tag):
                self._counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.is_active:
            self._counter[tag] -= 1

    def handle_data(self, data):
        if self.is_active:
            if not self._groups[-1].text:
                self._groups[-1].text = data.strip()
            self._groups[-1]._html += data
            self._groups[-1].text = self._groups[-1].inner_text()

    def handle_endtag(self, tag):
        if self.is_active:
            self._groups[-1]._html += f"</{tag}>"
            self._groups[-1].text = self._groups[-1].inner_text()
            self._counter[tag] -= 1

    def find(
        self,
        tag,
        attrs={},
        *,
        partial=True,
        mode="automatic",
        strict=None,
    ):
        self.tag = tag
        self.attrs = attrs
        self._partial = partial
        self._counter = Counter()
        self._groups = []
        self.feed(self._html)
        return self._groups


class Parser(HTMLParser):
    def __dir__(self):
        return ["attrs", "find", "get", "html", "strip", "tag", "text"]

    def __init__(self, html=None):
        """\
        Arguments:

        - html: content to parse
        """
        super().__init__()
        self._html = "" if not html else html
        self.tag = ""
        self.attrs = None
        self.text = ""

    def __repr__(self):
        return self.html

    def inner_text(self):
        element = re.match(r"<(.*)>(.*?)</\1>", re.sub(r"[\n\t\s]*", "", self._html))
        if element is None or self.find(element.group(1)) is None:
            return ""
        return self.find(element.group(1)).text

    @property
    def html(self):
        html = format(self._html)
        return html

    @classmethod
    def get(
        cls,
        url,
        params={},
        headers={},
    ):
        """\
        Intialize with gazpacho.get
        """
        html = get(url, params, headers)
        if not isinstance(html, str):
            raise Exception(f"Unable to retrieve contents from {url}")
        return cls(html)

    @staticmethod
    def is_void(tag):
        return tag in VOID_TAGS

    @property
    def is_active(self):
        return sum(self._counter.values()) > 0

    def handle_start(self, tag, attrs):
        html, attrs_dict = recover_html_and_attrs(tag, attrs)
        query_attrs = {} if not self.attrs else self.attrs
        matching = match(query_attrs, attrs_dict, partial=self._partial)

        if (tag == self.tag) and (matching) and (not self.is_active):
            self._groups.append(Soup())
            self._groups[-1].tag = tag
            self._groups[-1].attrs = attrs_dict
            self._groups[-1]._html += html
            self._counter[tag] += 1
            return

        if self.is_active:
            self._groups[-1]._html += html
            self._counter[tag] += 1

    def handle_starttag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.is_active:
            if self.is_void(tag):
                self._counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self.handle_start(tag, attrs)
        if self.is_active:
            self._counter[tag] -= 1

    def handle_data(self, data):
        if self.is_active:
            if not self._groups[-1].text:
                self._groups[-1].text = data.strip()
            self._groups[-1]._html += data
            self._groups[-1].text = self._groups[-1].inner_text()

    def handle_endtag(self, tag):
        if self.is_active:
            self._groups[-1]._html += f"</{tag}>"
            self._groups[-1].text = self._groups[-1].inner_text()
            self._counter[tag] -= 1

    def strip(self, whitespace=True):
        """\
        Strip brackets, tags, and attributes from inner text

        Arguments:

        - whitespace: remove extra whitespace characters

        Example:

        ```
        html = "<span>AB<b>C</b>D</span>"
        soup = Soup(html)
        soup.find("span").text
        # AB
        soup.strip()
        # ABCD
        ```
        """
        text = re.sub("<[^>]+>", "", self._html)
        if whitespace:
            text = " ".join(text.split())
        return text

    def _triage(self, groups, mode):
        """\
        Private method for .find -> return
        """
        automatic = ["auto", "automatic"]
        all = ["all", "list"]
        first = ["first"]
        last = ["last"]  # undocumented
        random = ["random"]  # undocumented

        if not groups:
            if mode in all:
                return []
            return None
        elif mode in automatic:
            if len(groups) == 1:
                return groups[0]
            return groups
        elif mode in all:
            return groups
        elif mode in first:
            return groups[0]
        elif mode in last:
            return groups[-1]
        elif mode in random:
            return sample(groups, k=1)[0]
        else:
            raise ValueError(mode)

    def find(
        self,
        tag,
        attrs={},
        *,
        partial=True,
        mode="automatic",
        strict=None,
    ):
        """\
        Return matching HTML elements

        Arguments:

        - tag: target element tag
        - attrs: target element attributes
        - partial: match on attributes
        - mode: dependent return behavior {'auto/automatic', 'all/list', 'first'}

        Deprecations:

        - strict: (as of 1.0) use partial=

        Examples:

        ```
        soup.find('p', {'class': 'a'})
        # [<p class="a">1</p>, <p class="a">2</p>]

        soup.find('p', {'class': 'a'}, mode='first')
        # <p class="a">1</p>

        result = soup.find('p', {'class': 'b'}, mode='auto')
        print(result)
        # <p class="b">3</p>

        print(result.text)
        # 3
        ```
        """
        self.tag = tag
        self.attrs = attrs
        self._partial = partial
        self._counter: Counter = Counter()
        self._groups: List["Soup"] = []
        self.feed(self._html)
        found = self._triage(self._groups, mode)
        return found
