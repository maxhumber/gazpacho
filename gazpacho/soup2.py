import re
import warnings
from collections import Counter
from html.parser import HTMLParser
from random import sample

class Soup(HTMLParser):
    def __init__(self, html=""):
        super().__init__()
        self._html = ""
        self.tag = ""
        self.attrs = None
        self.text = ""

    def __repr__(self):
        return self.html

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
    def recoverhtml_and_attrs(tag, attrs, startendtag=False):
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
    def html(self):
        html = format(self._html)
        return html

    @staticmethod
    def _void(tag: str):
        return tag in VOID_TAGS

    @property
    def _active(self):
        return sum(self._counter.values()) > 0

    def _handle_start(self, tag, attrs):
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

    def handle_starttag(self, tag, attrs):
        self._handle_start(tag, attrs)
        if self._active:
            if self._void(tag):
                self._counter[tag] -= 1

    def handle_startendtag(self, tag, attrs):
        self._handle_start(tag, attrs)
        if self._active:
            self._counter[tag] -= 1

    def handle_data(self, data):
        if self._active:
            if not self._groups[-1].text:
                self._groups[-1].text = data.strip()
            self._groups[-1]._html += data

    def handle_endtag(self, tag):
        if self._active:
            self._groups[-1]._html += f"</{tag}>"
            self._counter[tag] -= 1

    def strip(self, whitespace=True):
        text = re.sub("<[^>]+>", "", self._html)
        if whitespace:
            text = " ".join(text.split())
        return text

    def _triage(self, groups, mode):
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
        tag,
        attrs=None,
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
        found = self._triage(self._groups, mode)
        return found
