from urllib.parse import urlencode
from urllib.request import build_opener

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'

def get(url, params=None, headers=None):
    '''Get the content from a URL

    url: The URL for the webpage
    params: A dictionary of the param payload
    headers: A dictionary for the headers to be added

    Example:
    get('https://httpbin.org/anything', {'soup': 'gazpacho'})
    '''
    opener = build_opener()
    if params:
        url += '?' + urlencode(params)
    if headers:
        for h in headers.items():
            opener.addheaders = [h]
    else:
        opener.addheaders = [('User-Agent', DEFAULT_USER_AGENT)]
    with opener.open(url) as f:
        content = f.read().decode('utf-8')
    return content
