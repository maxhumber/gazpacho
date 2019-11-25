from gazpacho import Soup, get

html = """
<div class="foo-list">
  <span>This is some text, but it has fancy <b>bold tags</b> and even fancier <i>italic</i> tags</span>
  <p>There's some text here too</p>
</div>
"""

soup = Soup(html)
soup = soup.find("span")

soup.text
soup.html
soup.remove_tags()
