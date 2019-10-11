def match(a, b, strict=False):
    """Utility function to match two dictionaries

    Params:

    - a (dict): Query dictionary
    - b (dict): Dictionary to match
    - strict (bool): Require exact matching

    Examples:

    ```
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b)
    # True

    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b, strict=True)
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
    if not a:
        return True
    if not a and not b:
        return True
    if a and not b:
        return False
    for k, v in a.items():
        if not b.get(k):
            return False
        if strict:
            if v == b.get(k):
                continue
            else:
                return False
        if v in b.get(k):
            continue
        else:
            return False
    return True


def html_starttag_and_attrs(tag, attrs, startendtag=False):
    """Utility functon to reconstruct starttag and attrs

    Params:

    - tag (str): HTML element tag
    - attrs (list): HTML element attributes formatted as a list of tuples
    - startendtag (bool, False): Flag to handle startend tags

    Example:

    ```
    html_starttag_and_attrs('a', [('href', 'localhost:8000')])
    # ('<a href="localhost:8000">', {'href': 'localhost:8000'})
    ```
    """
    if attrs:
        attrs = dict(attrs)
        af = [f'{k}="{v}"' for k, v in attrs.items()]
        af = f' {" ".join(af)}'
    else:
        attrs = {}
        af = ""
    if startendtag:
        html = f"<{tag}{af} />"
    else:
        html = f"<{tag}{af}>"
    return html, attrs
