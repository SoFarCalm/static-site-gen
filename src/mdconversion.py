import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []

    if len(old_nodes) == 0:
        return new_nodes
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_node = old_node.text.split(delimiter)

        if len(split_node) % 2 == 0:
            raise Exception("Text is not valid markdown")
        else:
            created_nodes = []
            i = 0
            while i < len(split_node):
                if split_node[i].strip() == "":
                    i += 1
                    continue

                if (i == 0 or i % 2 == 0):
                    created_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    created_nodes.append(TextNode(split_node[i], text_type))
                i += 1

        new_nodes.extend(created_nodes)

    return new_nodes


def split_nodes_image(old_nodes: list):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        created_nodes = []
        text = old_node.text
        matches = extract_markdown_images(text)

        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        for match in matches:
            split_list = text.split(f"![{match[0]}]({match[1]})", 1)
            text = split_list[1]

            if len(split_list) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if split_list[0] != "":
                created_nodes.append(TextNode(split_list[0], TextType.TEXT))
        
            created_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))

        if len(text) > 0:
            created_nodes.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(created_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        created_nodes = []
        text = old_node.text
        matches = extract_markdown_links(text)

        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        for match in matches:
            split_list = text.split(f"[{match[0]}]({match[1]})", 1)
            text = split_list[1]

            if len(split_list) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if split_list[0] != "":
                created_nodes.append(TextNode(split_list[0], TextType.TEXT))
        
            created_nodes.append(TextNode(match[0], TextType.LINK, match[1]))

        if len(text) > 0:
            created_nodes.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(created_nodes)

    return new_nodes


def extract_markdown_images(text: str):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    image_tuples = re.findall(image_pattern, text)
    return image_tuples


def extract_markdown_links(text: str):
    link_pattern = r"\[(.*?)\]\((.*?)\)"
    link_tuples = re.findall(link_pattern, text)
    return link_tuples

def text_to_textnodes(text: str):
    node_list = []
    node = TextNode(text, TextType.TEXT)

    node_list = (split_nodes_delimiter([node], "**", TextType.BOLD))
    node_list = (split_nodes_delimiter(node_list, "_", TextType.ITALIC))
    node_list = (split_nodes_delimiter(node_list, "`", TextType.CODE))
    node_list = (split_nodes_image(node_list))
    node_list = (split_nodes_link(node_list))

    return node_list

def markdown_to_blocks(markdown: str):
    if markdown.strip() == "":
        return []

    all_blocks = markdown.split("\n\n")
    blocks = []

    for block in all_blocks:
        if block.strip() != '':
            blocks.append(block.strip())

    return blocks

def get_blocktype(block):
    if block == "":
        return BlockType.PARAGRAPH

    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1."):
        stripped_block = block.strip()
        split_block = stripped_block.split("\n")
        split_block = [line.strip() for line in split_block]

        for i in range(0, len(split_block)):
            if not (split_block[i].startswith(f"{i+1}.")):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_text_to_children(block_text: str):
    children = []

    text_nodes = text_to_textnodes(block_text)
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)

    return children

def block_text_to_code(block_text: str):
    stripped_text = block_text.strip()
    text = stripped_text[3:-3]
    if text[0] == '\n':
        text = text[1:]
    text = re.sub(r'  +', '', text)
    final_text = text.strip(" ")
    text_node = TextNode(final_text, TextType.CODE)
    html_node = text_node.text_node_to_html_node()
    return html_node


def get_html_header_level(block_text: str):
    level = 0
    while block_text.startswith("#"):
        level += 1
        if level == 6:
            return level

        block_text = block_text[1:]
    
    return level

def create_list_nodes(list_text: str):
    text = list_text.strip()
    list_items = text.split("\n")
    list_nodes = []

    for list_item in list_items:
        stripped_item = list_item.strip()
        item = stripped_item[2:].strip()
        if len(item) > 0:
            list_nodes.append(ParentNode("li", block_text_to_children(item)))

    return list_nodes


def replace_markdown(markdown: str):
    markdown = markdown.replace("\n", "")
    markdown = markdown.replace("    ", " ")

    return markdown


def markdown_to_html_node(markdown: str):
    block_nodes = []
    markdown_blocks = markdown_to_blocks(markdown)

    for markdown_block in markdown_blocks:
        block_type = get_blocktype(markdown_block)
        markdown_block_replaced = replace_markdown(markdown_block)

        if block_type == BlockType.HEADING:
            heading_level = get_html_header_level(markdown_block)
            block_nodes.append(ParentNode(f"{BlockType.HEADING.value}{heading_level}", block_text_to_children(markdown_block_replaced[heading_level:])))
        elif block_type == BlockType.CODE:
            block_nodes.append(ParentNode("pre", [block_text_to_code(markdown_block)]))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(ParentNode(BlockType.QUOTE.value, block_text_to_children(markdown_block_replaced[1:])))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(ParentNode(BlockType.UNORDERED_LIST.value, create_list_nodes(markdown_block)))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(ParentNode(BlockType.ORDERED_LIST.value, create_list_nodes(markdown_block)))
        else:
            block_nodes.append(ParentNode(BlockType.PARAGRAPH.value, block_text_to_children(markdown_block_replaced)))

    parent_node = ParentNode("div", block_nodes)
    return parent_node
