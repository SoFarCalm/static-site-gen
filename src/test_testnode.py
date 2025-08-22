import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr_non_url(self):
        node = TextNode("This is a test text node", TextType.BOLD)
        self.assertEqual(node.__repr__(), "TextNode(This is a test text node, TextType.BOLD)")
    
    def test_repr_url(self):
        node = TextNode("This is a test text node", TextType.LINK, "http://example.com")
        self.assertEqual(node.__repr__(), "TextNode(This is a test text node, TextType.LINK, http://example.com)")

    def test_url(self):
        node = TextNode("This is a url node", TextType.LINK)
        self.assertEqual(node.url, None)
    
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text_node_to_html_node(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_img_text_node_to_html_node(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "This is an image"})

    def test_link_text_node_to_html_node(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props, {"href": "http://example.com"})
        self.assertEqual(html_node.value, "This is a link")

if __name__ == "__main__":
    unittest.main()