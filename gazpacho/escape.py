import html

string = '<div tooltip-content="{"id": "7", "graph": "1->2"}">text</div>'
string

escaped = html.escape(string)
html.unescape(escaped)
