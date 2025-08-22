import re
from textnode import TextType, TextNode
from mdconversion import extract_markdown_links, extract_markdown_images

def main():
    test_string = "This is an image ![alt text](https://www.example.com/image.png)![my image](https://www.lonnie.com/image.png001)"
    new_nodes = []
    matches = extract_markdown_images(test_string)

    if matches:
        for match in matches:
            split_list = test_string.split(f"![{match[0]}]({match[1]})", 1)
            test_string = split_list[1]

            if len(split_list[0]) > 0:
                new_nodes.append(TextNode(split_list[0], TextType.TEXT))
        
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))

    if len(test_string) > 0:
        new_nodes.append(TextNode(test_string, TextType.TEXT))

    print(new_nodes)

main()
