import unittest

from textnode import TextNode, TextType
from mdconversion import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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
        self.assertEqual(extract_markdown_images(text), expected)

class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_markdown_links(self):
        text = "This is a [link](https://www.example.com) and another [link](https://www.example.org)"
        expected = [
            ("link", "https://www.example.com"),
            ("link", "https://www.example.org")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

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

if __name__ == "__main__":
    unittest.main()