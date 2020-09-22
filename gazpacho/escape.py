import html

string = '<div tooltip-content="{"id": "7", "graph": "1->2"}">text</div>'
string

escaped = html.escape(string)
html.unescape(escaped)

import xml.etree.ElementTree as ET

input = """
<div><div>Hi!</div></div>
"""

output = """\
<div>
  <div>Hi!</div>
</div>
"""


root = ET.fromstring(html)

ET.tostring(root, encoding="utf-8", method="html")
