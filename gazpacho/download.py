from urllib.request import urlretrieve
from gazpacho.utils import sanitize

from io import BytesIO
from urllib.request import urlopen

# does this make sense? for multiple usage, try with wav? and videos?

class Bytes(BytesIO):
    def __init__(self, url):
        contents = urlopen(url).read()
        super().__init__(contents)
        self.url = url

    def __repr__(self):
        return f'Bytes("{self.url}")'


def download(url, path=None):
    url = sanitize(url)
    if not path:
        return Bytes(url)
    urlretrieve(url, path)

# from gazpacho import download
# asset()

# testing

from PIL import Image

url = "https://scrape.world/static/fish_1.png"
path = "test_image.png"

bo = Bytes(url)
Image.open(bo)

download(url, path)
download(url)


soup.download("/source")


#
