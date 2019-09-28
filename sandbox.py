from gazpacho import get

html = get('https://maxhumber.com/')
print(html)

html = '''<!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-89691472-1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-89691472-1');
    </script>
    <!-- Required meta tags -->
    <title>Max Humber</title>'''

import re

x = re.sub('\<script(.*?)\<\/script\>', '', html)
print(x)


var x = "abc.cde:abc";

re.sub('\<script[^\<\/script\>]*\<\/script\>', '', html)
 "abc abc"

import xml.etree.ElementTree as ET
root = ET.fromstring(html)


from xml.dom import minidom
x = minidom.parseString(html, )
x.toprettyxml()
