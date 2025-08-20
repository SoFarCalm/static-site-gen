import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "I'm node 1!")
        node2 = HTMLNode("p", "I'm node 1!")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("p", "text that goes inside paragraph", [] , {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.__repr__(), 
            "HTMLNode(p, text that goes inside paragraph, [], {'href': 'https://www.google.com', 'target': '_blank'})"
            )

    def test_props_to_html(self):
        node = HTMLNode("h1", "header of my html", [] , {"href": "https://www.google.com", "target": "_blank"})
        test_props_string = node.props_to_html()
        self.assertEqual(test_props_string, 'href="https://www.google.com" target="_blank" ')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_siblings(self):
        child_node = LeafNode("p", 'sibling1')
        child_node2 = LeafNode("p", 'sibling2')
        child_node3 = LeafNode("p", 'sibling3')
        parent_node = ParentNode('div', [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>sibling1</p><p>sibling2</p><p>sibling3</p></div>"
        )
    
    def test_to_html_no_child(self):
        parent_node = ParentNode('div', None)
        self.assertRaises(ValueError)
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("p", 'sibling1')
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError)

if __name__ == "__main__":
    unittest.main()