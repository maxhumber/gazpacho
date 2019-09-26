def match(query_attrs, attrs):
    '''Match a query dictionary to an attrs dictionary'''
    if not query_attrs:
        return True
    if not query_attrs and not attrs:
        return True
    if query_attrs and not attrs:
        return False
    bools = []
    for k, v in query_attrs.items():
        if not attrs.get(k):
            bools.append(False)
        elif v in attrs.get(k):
            bools.append(True)
        else:
            bools.append(False)
    return all(bools)

def html_starttag_and_attrs(tag, attrs, startendtag=False):
    '''Reconstruct starttag and convert attrs to a dictionary'''
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
