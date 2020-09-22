from urllib.request import urlretrieve
from gazpacho.utils import sanitize

from io import BytesIO
from urllib.request import urlopen


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


# testing

from PIL import Image

url = "https://scrape.world/static/fish_1.png"
path = "test_image.png"

bo = Bytes(url)
Image.open(bo)

download(url, path)
download(url)
