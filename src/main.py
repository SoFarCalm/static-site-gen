import re
import sys
from variables import STATIC_PATH, PUBLIC_PATH, CONTENT_PATH, TEMPLATE_PATH, DEST_PATH
from textnode import TextType, TextNode
from mdconversion import *
from copy_static import copy_static_files

STATIC_PATH = "static"
CONTENT_PATH = "content"
TEMPLATE_PATH = "template.html"
DEST_PATH = "docs"

def main():

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    copy_static_files(STATIC_PATH, DEST_PATH)
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, DEST_PATH, base_path)

main()