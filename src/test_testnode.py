import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a test text node", TextType.TEXT)
        print(node)
    
    def test_url(self):
        node = TextNode("This is a url node", TextType.LINK)
        if node.url is None:
            print("Node does not have a URL")


if __name__ == "__main__":
    unittest.main()