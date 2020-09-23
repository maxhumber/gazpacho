from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
import random
import re
from typing import Dict, Optional, Tuple, Union, List

from .utils import match, html_starttag_and_attrs
from .get import get

class Soup(HTMLParser):
    """\
    HTML Soup Parser

    Attributes:

    - html: content to parse
    - tag: element tag
    - attrs: element attributes
    - text: text data

    Methods:

    - find: matching content by tag (and attributes)
    - strip:
    - get: initialize instance with gazpacho.get
    - post: initialize instance with gazpacho.post

    Examples:

    ```
    >>> from gazpacho import Soup

    >>> html = "<div><p class='a'>1</p><p class='a'>2</p><p class='b'>3</p></div>"
    >>> url = "https://www.exaxmple.com"

    >>> soup = Soup(html)
    >>> soup = Soup.get(url)
    >>> soup = Soup.post(url, {"foo": "bar"})
    ```
    """
    def __init__(self, html: Optional[str] = None) -> None:
        """\
        Params:

        - html: content to parse
        """
        super().__init__()
        self.html = "" if not html else html
        self.tag = None
        self.attrs = None
        self.text = None

    def __dir__(self):
        ex = sorted(re.findall("(?<=\-\s)(.*)(?=\:)", self.__doc__))
        return ex

    def __repr__(self) -> str:
        return self.html

    # need to write tests
    @classmethod
    def get(
        cls,
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Soup:
        """\
        ...
        TODO
        ...
        """
        html = get(url, params, headers)
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

    def _handle_start(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        html, attrs = html_starttag_and_attrs(tag, attrs)
        matching = match(self.attrs, attrs, partial=self.partial)

        if (tag == self.tag) and (matching) and (not self._active):
            self.groups.append(Soup())
            self.groups[-1].tag = tag
            self.groups[-1].attrs = attrs
            self.groups[-1].html += html
            self.counter[tag] += 1
            return

        if self._active:
            self.groups[-1].html += html
            self.counter[tag] += 1

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        self._handle_start(tag, attrs)
        if self._active:
            if self._void(tag):
                self.counter[tag] -= 1

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
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
        Remove brackets, tags, and attributes

        Params:

        - whitespace: remove extra whitespace

        Example:

        ```
        >>> html = "<span>AB<b>C</b>D</span>"
        >>> soup = Soup(html)
        >>> soup.find("span").text
        AB
        >>> soup.strip()
        ABCD
        ```
        """
        text = re.sub("<[^>]+>", "", self.html)
        if whitespace:
            text = " ".join(text.split())
        return text

    # # deprecate
    # def remove_tags(self, strip: bool = True) -> str:
    #     text = re.sub("<[^>]+>", "", self.html)
    #     if strip:
    #         text = " ".join(text.split())
    #     return text

    # need a strict deprecation message here
    # accept strict as an argument for backwards compat
    def find(
        self,
        tag: str,
        attrs: Optional[Dict[str, str]] = None,
        *,
        mode: str = "auto",
        partial: bool = True,
        strict: Optional[bool] = None,
    ) -> Optional[Union[List[Soup], Soup]]:
        """\
        Return matching HTML elements

        Params:

        - tag (str): HTML element tag to find
        - attrs (dict, optional): HTML element attributes to match
        - mode (str, 'auto'): Element(s) to return {'auto', 'all', 'first'}
        - strict (bool, False): Require exact attribute matching

        Examples:

        ```
        >>> soup.find('p', {'class': 'a'})
        [<p class="a">1</p>, <p class="a">2</p>]

        >>> soup.find('p', {'class': 'a'}, mode='first')
        <p class="a">1</p>

        >>> result = soup.find('p', {'class': 'b'}, mode='auto')
        >>> print(result)
        <p class="b">3</p>

        >>> print(result.text)
        3
        ```
        """
        # deprecation
        if strict is not None:
            raise

        self.tag = tag
        self.attrs = attrs
        self.partial = partial
        self.counter = Counter()
        self.groups = []
        self.feed(self.html)

        # does this make it more confusing? Undecided
        # first
        modeX = ["first", "head"]  # leave off head

        # last
        modeX = ["last", "tail"]

        # random
        modeX = ["one", "random", "sample"]

        # all
        modeX = ["all", "list"]

        # automatic
        modeX = ["auto", "automatic"]  # could probably make this no problem

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
