from urllib.request import urlretrieve
from gazpacho.utils import sanitize

from io import BytesIO
from urllib.request import urlopen

url = "https://scrape.world/static/fish_1.png"
path = "test_image.png"

urlretrieve(url, path)

####

def download(url, path=None):
    url = sanitize(url)
    if not path:
        return BytesIO(urlopen(url).read())
    urlretrieve(url, path)

from PIL import Image

Image.open(download(url))

download(url, "test_image.png")


# something more descriptive about BytesIO
