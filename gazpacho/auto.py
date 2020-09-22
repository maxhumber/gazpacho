from gazpacho import Soup

soup = Soup.get("https://www.programiz.com/python-programming/methods/built-in/classmethod")

tag = '<span class="mw-headline" id="History">'

# if just alpha -> normal tag

html = """\
    <div>
        <img src="hi.png">
        <div id="price">19.99</div>
        <div id="price">5.00</div>
        <div id="price">2.99</div>
        <div>Not a price</div>
    </div>
"""

import re

target = 19.99
found_html = re.findall(f'<.*>{target}</.*>', html)[0]
found_html


tag = re.findall("(?<=\<)(.*?)(?=\s)", found_html)[0]
attrs_string = re.findall("(?<=\s)(.*?)(?=\>)", found_html)[0]

# split

attrs_string = 'id="price" class="sup"'
attrs_raw = attrs_string.split(' ')
attrs_list = [a.split('=') for a in attrs_raw]

import json

attrs = {k: json.loads(v) for k, v in attrs_list}
attrs


soup = Soup(found_html)
soup.find('div', {'id': 'price'}).text

found_html






#
