import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "I'm node 1!")
        node2 = HTMLNode("p", "I'm node 1!")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("p", "text that goes inside paragraph", [] , {"href": "https://www.google.com", "target": "_blank"})
        print(node)

    def test_props_to_html(self):
        node = HTMLNode("h1", "header of my html", [] , {"href": "https://www.google.com", "target": "_blank"})
        test_props_string = node.props_to_html()
        print(test_props_string)

if __name__ == "__main__":
    unittest.main()