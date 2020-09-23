## API > separate library?

# Soup.reverse_find(url, target)
# AutoSoup()
# Soup.recipe("")
# AutoScrape()
# Recipe()
# auto_scrape()

# Potential options
# soup.build_find("19.99")
# soup.inverse_find()
# soup.reverse_find()
# soup.find_pattern()
# soup.auto()
# soup.try()
# soup.try_to_find()
# soup.build("19.99")
# soup.find_similar("")
# soup.build_find("")
# soup.auto_find("19.99")
# soup.generate_code("19.99")
# soup.find_tag_and_attrs()
# soup.reverse_find()
# soup.discover
# soup.attempt
# soup.recipe # too cheesy

###

from gazpacho import Soup

import re
import json


def find_block(target, html):
    return re.findall(f"<.*>{target}</.*>", html)[0]


def extract_tag_and_attrs(block):
    tag = re.findall("(?<=\<)(.*?)(?=\s)", block)[0]
    attrs_string = re.findall("(?<=\s)(.*?)(?=\>)", block)[0]
    attrs_raw = attrs_string.split(" ")
    attrs_list = [a.split("=") for a in attrs_raw]
    attrs = {k: json.loads(v) for k, v in attrs_list}
    return tag, attrs


# test

html = """\
    <div>
        <img src="hi.png">
        <div id="price">19.99</div>
        <div id="price">5.00</div>
        <div id="price">2.99</div>
        <div>Not a price</div>
    </div>
"""

target = "19.99"

block = find_block(target, html)
tag, attrs = extract_tag_and_attrs(block)

soup = Soup(html)

results = soup.find(tag, attrs)
target in [r.text for r in results]

# template

url = "www.example.com"

template = f"""
from gazpacho import get, Soup

url = {url}
html = get(url)
soup = Soup(html)

soup.find({tag}, {attrs})
"""

print(template)


#
