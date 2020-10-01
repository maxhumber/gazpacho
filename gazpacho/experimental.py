import json
import re
from typing import List, Union

from gazpacho import Soup, get

def find_block(target, html):
    target = re.escape(target)
    result = re.findall(f"<.*>{target}</.*?>", html)[0]
    if not result.startswith("<"):
        result = "<" + result.split('><')[-1]
    return result.replace("<<", '<')

def extract_tag_and_attrs(block):
    tag = re.findall("(?<=\<)(.*?)(?=\s|\>)", block)[0]
    try:
        attrs_string = re.findall("(?<=\s)(.*?)(?=\>)", block)[0]
    except IndexError:
        attrs_string = ""
    if (attrs_string) and ("</" not in attrs_string):
        attrs_raw = re.split("(?<=\'|\")\s", attrs_string)
        attrs_list = [a.split("=") for a in attrs_raw]
        attrs = {k: json.loads(v) for k, v in attrs_list}
    else:
        attrs = {}
    return tag, attrs

def similar(target, html):
    soup = Soup(html)
    block = find_block(target, html)
    tag, attrs = extract_tag_and_attrs(block)
    results = soup.find(tag, attrs, mode="all")
    if target in [r.text for r in results]:
        return results

def similar2(html: str, positive: Union[str, List[str]], negative=None):
    if isinstance(positive, str):
        positive = list(positive)
    for target in positive:
        similar(target, html)


url = "https://scrape.world/spend"
html = get(url)

target1 = "Toronto Pine Needles"
block1 = find_block(target1, html)
tag1, attrs1 = extract_tag_and_attrs(block1)


target2 = "Arizona Dingos"
block2 = find_block(target2, html)
tag2, attrs2 = extract_tag_and_attrs(block2)

tag1
tag2

attrs1
attrs2


def longest_common_substring(strings: List[str]) -> str:
    lcs = ""
    if len(strings) > 1 and len(strings[0]) > 0:
        for i in range(len(strings[0])):
            for j in range(len(strings[0]) - i + 1):
                if j > len(lcs) and all(strings[0][i : i + j] in x for x in strings):
                    lcs = strings[0][i : i + j]
    return lcs


# related
# similar
# coincident
# coincidental
# congruent
# parallel
# like
# near
# related
