import re
from xml.dom.minidom import parseString as string_to_dom
from xml.parsers.expat import ExpatError

VOID_TAGS = [
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


def format(html, fail=False):
    """\
    Indent and format html

    Arguments:

    - html: string to format
    - fail: allowed to fail as a boolean

    Example:
    ```
    html = "<ul><li>Item</li><li>Item</li></ul>"
    print(format(html))
    # <ul>
    #   <li>Item</li>
    #   <li>Item</li>
    # </ul>
    ```
    """
    try:
        html_closed_voids = re.sub(
            fr'(<({"|".join(VOID_TAGS)})[^/>]*)(>)', fr"\1/\3", html
        )
        dom = string_to_dom(html_closed_voids)
        ugly = dom.toprettyxml(indent="  ")
        split = list(filter(lambda x: len(x.strip()), ugly.split("\n")))[1:]
        html_joined = "\n".join(split)
        html = re.sub(fr'(<)({"|".join(VOID_TAGS)})(.*)(\/>)', fr"\1\2\3>", html_joined)
    except ExpatError as error:
        if fail:
            raise error
    return html


def match(a, b, *, partial=False):
    """\
    Match two dictionaries

    Arguments:

    - a: query dict
    - b: dict to match
    - partial: allow partial match

    Examples:

    ```
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b, partial=True)
    # True

    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b)
    # False

    a = {}
    b = {'foo': 'bar'}
    match(a, b)
    # True

    a = {}
    b = {}
    match(a, b)
    # True
    ```
    """
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


def recover_html_and_attrs(tag, attrs, startendtag=False):
    """\
    Recover html and attrs from HTMLParser feed

    Arguments:

    - tag: element tag
    - attrs: element attributes formatted as a dict
    - startendtag: boolean if start-end tag

    Example:

    ```
    recover_html_and_attrs('img', [('src', 'example.png')])
    # ("<img src='example.png'>", {'src': 'example.png'})
    ```
    """
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
