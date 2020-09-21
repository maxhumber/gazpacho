import html

string = '<div tooltip-content="{"id": "7", "graph": "1->2"}">text</div>'
string

escaped = html.escape(string)
html.unescape(escaped)

import re

tagfind_tolerant = re.compile(r'([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*')
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][^\t\n\r\f />\x00]*       # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
         (?:\s*,)*                   # possibly followed by a comma
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)
endendtag = re.compile('>')
# the HTML 5 spec, section 8.1.2.2, doesn't allow spaces between
# </ and the tag name, so maybe this should be fixed
endtagfind = re.compile(r'</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>')

rawdata = '<div tooltip-content="{"id": "7", "graph": "1->2"}">text</div>'

i = 0
match = tagfind_tolerant.match(rawdata, i+1)
k = match.end()
self.lasttag = tag = match.group(1).lower()
while k < endpos:
    m = attrfind_tolerant.match(rawdata, k)
    if not m:
        break
    attrname, rest, attrvalue = m.group(1, 2, 3)
    if not rest:
        attrvalue = None
    elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
         attrvalue[:1] == '"' == attrvalue[-1:]:
        attrvalue = attrvalue[1:-1]
    if attrvalue:
        attrvalue = unescape(attrvalue)
    attrs.append((attrname.lower(), attrvalue))
    k = m.end()
