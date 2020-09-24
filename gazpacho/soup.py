from collections import Counter
from html.parser import HTMLParser
from random import sample
import re
from typing import Any, Dict, Optional, Tuple, Union, List
import warnings

from .get import get
from .utils import match, recover_html_and_attrs


class Soup(HTMLParser):
    """\
    HTML Soup Parser

    Attributes:

    - html: content to parse
    - tag: element to match
    - attrs: element attributes to match
    - text: inner data

    Methods:

    - find: matching content by element tag (and attributes)
    - strip: brackets, tags, and attributes from inner data
    - get: alternate initializer

    Deprecations:

    - remove_tags: (as of 1.0) use strip

    Examples:

    ```
    from gazpacho import Soup

    html = "<div><p class='a'>1</p><p class='a'>2</p><p class='b'>3</p></div>"
    url = "https://www.gazpacho.xyz"

    soup = Soup(html)
    soup = Soup.get(url)
    ```
    """

    def __init__(self, html: Optional[str] = None) -> None:
        """\
        Arguments:

        - html: content to parse
        """
        super().__init__()
        self.html = "" if not html else html
        self.tag: Optional[str] = None
        self.attrs: Optional[Dict[Any, Any]] = None
        self.text: Optional[str] = None

    def __dir__(self):
        return ["attrs", "find", "get", "html", "strip", "tag", "text"]

    def __repr__(self) -> str:
        return self.html

    @classmethod
    def get(
        cls,
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "Soup":
        """\
        Intialize with gazpacho.get
        """
        html = get(url, params, headers)
        if not isinstance(html, str):
            raise Exception(f"Unable to retrieve contents from {url}")
        return cls(html)

    @property
    def _active(self) -> bool:
        return sum(self.counter.values()) > 0

    @staticmethod
    def _void(tag: str) -> bool:
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

    def _handle_start(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        html, attrs_dict = recover_html_and_attrs(tag, attrs)
        query_attrs = {} if not self.attrs else self.attrs
        matching = match(query_attrs, attrs_dict, partial=self.partial)

        if (tag == self.tag) and (matching) and (not self._active):
            self.groups.append(Soup())
            self.groups[-1].tag = tag
            self.groups[-1].attrs = attrs_dict
            self.groups[-1].html += html
            self.counter[tag] += 1
            return

        if self._active:
            self.groups[-1].html += html
            self.counter[tag] += 1

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self._handle_start(tag, attrs)
        if self._active:
            if self._void(tag):
                self.counter[tag] -= 1

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        self._handle_start(tag, attrs)
        if self._active:
            self.counter[tag] -= 1

    def handle_data(self, data: str) -> None:
        if self._active:
            if self.groups[-1].text is None:
                self.groups[-1].text = data.strip()
            self.groups[-1].html += data

    def handle_endtag(self, tag: str) -> None:
        if self._active:
            self.groups[-1].html += f"</{tag}>"
            self.counter[tag] -= 1

    def strip(self, whitespace: bool = True) -> str:
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
        text = re.sub("<[^>]+>", "", self.html)
        if whitespace:
            text = " ".join(text.split())
        return text

    def remove_tags(self, strip: bool = True) -> str:
        """\
        Now: .strip()
        """
        message = "Marked for removal; use .strip()"
        warnings.warn(message, category=FutureWarning, stacklevel=2)
        return self.strip(whitespace=strip)

    def find(
        self,
        tag: str,
        attrs: Optional[Dict[str, str]] = None,
        *,
        partial: bool = True,
        mode: str = "automatic",
        strict: Optional[bool] = None,
    ) -> Optional[Union[List["Soup"], "Soup"]]:
        """\
        Return matching HTML elements

        Arguments:

        - tag: target element tag
        - attrs: target element attributes
        - partial: match on attributes
        - mode: override return behavior {'auto/automatic', 'all/list', 'first'}

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
        self.counter: Counter = Counter()
        self.groups: List = []
        self.tag = tag
        self.attrs = attrs
        self.partial = partial

        if strict is not None:
            message = "Marked for removal; use partial="
            warnings.warn(message, category=FutureWarning, stacklevel=2)
            partial = not strict

        self.feed(self.html)

        automatic = ["auto", "automatic"]
        all = ["all", "list"]
        first = ["first"]
        last = ["last"]  # undocumented
        random = ["random"]  # undocumented

        if not self.groups:
            if mode in all:
                return []
            else:
                return None
        elif mode in automatic:
            if len(self.groups) == 1:
                return self.groups[0]
            else:
                return self.groups
        elif mode in all:
            return self.groups
        elif mode in first:
            return self.groups[0]
        elif mode in last:
            return self.groups[-1]
        elif mode in random:
            return sample(self.groups, k=1)[0]
        else:
            raise ValueError(mode)
