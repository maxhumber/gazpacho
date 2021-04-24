import re
import warnings
from collections import Counter
from html.parser import HTMLParser
from random import sample


class Parser(HTMLParser):
    def __init__(self, html=""):
        super().__init__()
        self.html = html

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
    def is_active(self):
        return sum(self._counter.values()) > 0

    def handle_start(self, tag, attrs):
        html, attrs_dict = self.recoverhtml_and_attrs(tag, attrs)
        query_attrs = {} if not self.attrs else self.attrs
        matching = self.match(query_attrs, attrs_dict, partial=self._partial)

        if (tag == self.tag) and (matching) and (not self.is_active):
            self._groups.append(Parser())
            self._groups[-1].tag = tag
            self._groups[-1].attrs = attrs_dict
            self._groups[-1].html += html
            self._counter[tag] += 1
            return

        if self.is_active:
            self._groups[-1].html += html
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
            self._groups[-1].html += data
            self._groups[-1].text = self._groups[-1].inner_text()

    def handle_endtag(self, tag):
        if self.is_active:
            self._groups[-1].html += f"</{tag}>"
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
        self.feed(self.html)
        return self._groups


html = """\
<div class="foo" id="bar">
  <p>'IDK!'</p>
  <br/>
  <div class='baz'>
    <div>
      <span>Hi</span>
    </div>
  </div>
  <p id='blarg'>Try for 2</p>
  <div class='baz'>Oh No!</div>
</div>
"""

parser = Parser(html)
parser.find("p")
