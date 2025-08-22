import re
from textnode import TextNode, TextType

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

        if matches:
            for match in matches:
                split_list = text.split(f"![{match[0]}]({match[1]})", 1)
                text = split_list[1]

                if len(split_list[0]) > 0:
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

        if matches:
            for match in matches:
                split_list = text.split(f"[{match[0]}]({match[1]})", 1)
                text = split_list[1]

                if len(split_list[0]) > 0:
                    created_nodes.append(TextNode(split_list[0], TextType.TEXT))
            
                created_nodes.append(TextNode(match[0], TextType.LINK, match[1]))

        if len(text) > 0:
            created_nodes.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(created_nodes)

    return new_nodes


def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    image_tuples = re.findall(image_pattern, text)
    return image_tuples


def extract_markdown_links(text):
    link_pattern = r"\[(.*?)\]\((.*?)\)"
    link_tuples = re.findall(link_pattern, text)
    return link_tuples