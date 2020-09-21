from urllib.request import Request, urlopen
import datetime
import json

from gazpacho.utils import sanitize

url = "https://scrape.world/demand"

data = {
    "date": str(datetime.datetime.now()),
    "temperature": 21
}

def post(url, data):
    url = sanitize(url)
    data = bytes(json.dumps(data).encode("utf-8"))
    request = Request(url=url, data=data, method="POST")
    request.add_header("Content-type", "application/json; charset=UTF-8")
    with urlopen(request) as response:
        response = json.loads(response.read().decode("utf-8"))
    return response

post(url, data)
