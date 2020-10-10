from gazpacho import Soup

html = """<p>&pound;682m</p>"""
soup = Soup(html)
res= soup.find('p')
print(res.text)