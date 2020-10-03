import re
import warnings
from collections import Counter
from html.parser import HTMLParser
from random import sample
from typing import Any, Dict, List, Optional, Tuple, Union

from .get import get
from .utils import VOID_TAGS, ParserAttrs, format, match, recover_html_and_attrs


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

    def __dir__(self):
        return ["attrs", "find", "get", "html", "strip", "tag", "text"]

    def __init__(self, html: Optional[str] = None) -> None:
        """\
        Arguments:

        - html: content to parse
        """
        super().__init__()
        self._html = "" if not html else html
        self.tag: str = ""
        self.attrs: Optional[Dict[str, Any]] = None
        self.text: str = ""

    def __repr__(self) -> str:
        return self.html

    @property
    def html(self) -> str:
        html = format(self._html)
        return html

    @classmethod
    def get(
        cls,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> "Soup":
        """\
        Intialize with gazpacho.get
        """
        html = get(url, params, headers)
        if not isinstance(html, str):
            raise Exception(f"Unable to retrieve contents from {url}")
        return cls(html)

    @staticmethod
    def _void(tag: str) -> bool:
        return tag in VOID_TAGS

    @property
    def _active(self) -> bool:
        return sum(self._counter.values()) > 0

    def _handle_start(self, tag: str, attrs: ParserAttrs) -> None:
        html, attrs_dict = recover_html_and_attrs(tag, attrs)
        query_attrs = {} if not self.attrs else self.attrs
        matching = match(query_attrs, attrs_dict, partial=self._partial)

        if (tag == self.tag) and (matching) and (not self._active):
            self._groups.append(Soup())
            self._groups[-1].tag = tag
            self._groups[-1].attrs = attrs_dict
            self._groups[-1]._html += html
            self._counter[tag] += 1
            return

        if self._active:
            self._groups[-1]._html += html
            self._counter[tag] += 1

    def handle_starttag(self, tag: str, attrs: ParserAttrs) -> None:
        self._handle_start(tag, attrs)
        if self._active:
            if self._void(tag):
                self._counter[tag] -= 1

    def handle_startendtag(self, tag: str, attrs: ParserAttrs) -> None:
        self._handle_start(tag, attrs)
        if self._active:
            self._counter[tag] -= 1

    def handle_data(self, data: str) -> None:
        if self._active:
            if not self._groups[-1].text:
                self._groups[-1].text = data.strip()
            self._groups[-1]._html += data

    def handle_endtag(self, tag: str) -> None:
        if self._active:
            self._groups[-1]._html += f"</{tag}>"
            self._counter[tag] -= 1

    def remove_tags(self, strip: bool = True) -> str:
        """\
        Now: .strip()
        """
        message = "Marked for removal; use .strip()"
        warnings.warn(message, category=FutureWarning, stacklevel=2)
        return self.strip(whitespace=strip)

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
        text = re.sub("<[^>]+>", "", self._html)
        if whitespace:
            text = " ".join(text.split())
        return text

    def _triage(
        self, groups: List["Soup"], mode: str
    ) -> Optional[Union[List["Soup"], "Soup"]]:
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
            else:
                return None
        elif mode in automatic:
            if len(groups) == 1:
                return groups[0]
            else:
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
        tag: str,
        attrs: Optional[Dict[str, Any]] = None,
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

        if strict is not None:
            message = "Marked for removal; use partial="
            warnings.warn(message, category=FutureWarning, stacklevel=2)
            partial = not strict

        self.feed(self._html)
        found = self._triage(self._groups, mode)

        return found
