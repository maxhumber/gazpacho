def match(a, b, strict=False):
    '''A utility function to match two dictionaries

    - a (dict): The query dictionary
    - b (dict): The dictionary to match
    - strict (bool): Require exact matching

    Examples:

    ```
    a = {'foo': 'bar'}
    b = {'foo': 'bar baz'}
    match(a, b)
    # True

    a = {}
    b = {'foo': 'bar'}
    match(a, b)
    # True
    ```
    '''
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
    '''A utility functon to reconstruct starttag and attrs

    - tag (str): HTML tag
    - attrs (list): A list of tuples for HTML tag attributes
    - startendtag (bool): A flag to handle startend tags

    Example:

    ```
    html_starttag_and_attrs('a', [('href', 'localhost:8000')])
    # ('<a href="localhost:8000">', {'href': 'localhost:8000'})
    ```
    '''
    if attrs:
        attrs = dict(attrs)
        af = [f'{k}="{v}"' for k, v in attrs.items()]
        af = f' {" ".join(af)}'
    else:
        attrs = {}
        af = ''
    if startendtag:
        html = f'<{tag}{af} />'
    else:
        html = f'<{tag}{af}>'
    return html, attrs
