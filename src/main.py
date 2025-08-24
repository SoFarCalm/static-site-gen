import re
from textnode import TextType, TextNode
from mdconversion import *

def main():

    md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

    print(block_text_to_code(md))
    # node = markdown_to_html_node(md)
    # html = node.to_html()
    # print(node)

main()
