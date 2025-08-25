import re
from textnode import TextType, TextNode
from mdconversion import *
from copy_static import copy_static_files

def main():

    src_path = '/home/lonniedev/workspace/github/sofarcalm/static-site-gen/static'
    dest_path = '/home/lonniedev/workspace/github/sofarcalm/static-site-gen/public'

    copy_static_files(src_path, dest_path)

main()
