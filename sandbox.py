from gazpacho import Soup

html = """
<div class="foo-list">
  <a class="foo" href="/foo/1">
    <div class="foo-image-container">
      <img src="image.jpg">
    </div>
  </a>
  <a class="foo" href="/foo/2">
    <div class="foo-image-container">
      <img src="image.jpg">
    </div>
  </a>
</div>
"""

soup = Soup(html)
soup.find("a", {"class": "foo"})
