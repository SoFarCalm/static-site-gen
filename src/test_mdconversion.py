import unittest

from textnode import TextNode, TextType
from mdconversion import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")

class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](https://www.example.com/image.png), here is another image ![my image](https://www.lonnie.com/image.png001)"
        expected = [
            ("alt text", "https://www.example.com/image.png"),
            ("my image", "https://www.lonnie.com/image.png001")
        ]
        self.assertListEqual(extract_markdown_images(text), expected)

class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_markdown_links(self):
        text = "This is a [link](https://www.example.com) and another [link](https://www.example.org)"
        expected = [
            ("link", "https://www.example.com"),
            ("link", "https://www.example.org")
        ]
        self.assertListEqual(extract_markdown_links(text), expected)

class TestSplitNodesImages(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/lonnie.png) and another ![second image](https://i.imgur.com/currie.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/lonnie.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/currie.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLinks(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [link](https://www.example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.org"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(text_to_textnodes(text), expected)
    
    def test_text_to_textnodes_link(self):
        text = "[link](https://boot.dev)"
        expected = [
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_empty(self):
        text = ""
        expected = []
        self.assertListEqual(text_to_textnodes(text), expected)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertListEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_empty(self):
        markdown = ""
        expected = []
        self.assertListEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_empty(self):
        markdown = "       "
        expected = []
        self.assertListEqual(markdown_to_blocks(markdown), expected)

class TestGetBlockType(unittest.TestCase):

    def test_get_blocktype(self):
        self.assertEqual(get_blocktype("# Heading"), BlockType.HEADING)
        self.assertEqual(get_blocktype("```code```"), BlockType.CODE)
        self.assertEqual(get_blocktype("```code"), BlockType.PARAGRAPH)
        self.assertEqual(get_blocktype("> Quote"), BlockType.QUOTE)
        self.assertEqual(get_blocktype("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(get_blocktype("1. Ordered item\n2. Another ordered item\n3. Yet another ordered item"), BlockType.ORDERED_LIST)
        self.assertEqual(get_blocktype("1. Ordered item\n2. Another ordered item\n4. Yet another ordered item"), BlockType.PARAGRAPH)
        self.assertEqual(get_blocktype("Just a paragraph"), BlockType.PARAGRAPH)

# class TestBlockToChildren(unittest.TestCase):

#     def test_block_text_to_children(self):
#         block = """
#     This is **bolded** paragraph
#     text in a p
#     tag here

#     This is another paragraph with _italic_ text and `code` here

#     """
#         expected = [
#             ParentNode("h1", [TextNode("Heading", TextType.TEXT)])
#         ]
#         self.assertListEqual(block_text_to_children(block), expected)

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node(self):
        markdown = "# Heading\n\nThis is a paragraph."
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><h1> Heading</h1><p>This is a paragraph.</p></div>")

    def test_markdown_to_html_node_empty(self):
        markdown = ""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div></div>")

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
    - Item 1
    - Item 2
    - Item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. Item 1
    2. Item 2
    3. Item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()