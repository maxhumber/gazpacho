import re
from xml.dom.minidom import parseString as string_to_dom
from xml.parsers.expat import ExpatError


def format(html, fail=False):
    """\
    Indent and format html

    Arguments:

    - html: string to format
    - fail: allowed to fail as a boolean

    Example:
    ```
    html = "<ul><li>Item</li><li>Item</li></ul>"
    print(format(html))
    # <ul>
    #   <li>Item</li>
    #   <li>Item</li>
    # </ul>
    ```
    """
    try:
        html_closed_voids = re.sub(
            fr'(<({"|".join(VOID_TAGS)})[^/>]*)(>)', fr"\1/\3", html
        )
        dom = string_to_dom(html_closed_voids)
        ugly = dom.toprettyxml(indent="  ")
        split = list(filter(lambda x: len(x.strip()), ugly.split("\n")))[1:]
        html_joined = "\n".join(split)
        html = re.sub(fr'(<)({"|".join(VOID_TAGS)})(.*)(\/>)', fr"\1\2\3>", html_joined)
    except ExpatError as error:
        if fail:
            raise error
    return html
