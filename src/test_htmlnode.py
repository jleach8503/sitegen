import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected = 'href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        children = [HTMLNode("p", "Some paragraph")]
        node = HTMLNode("a", "somevalue", children, props)
        expected = 'HTMLNode(a, somevalue, [HTMLNode(p, Some paragraph, None, )], href="https://www.google.com" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_empty_leaf_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("a", "somevalue", props)
        expected = 'LeafNode(a, somevalue, href="https://www.google.com" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_empty_leaf_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()
        


if __name__ == "__main__":
    unittest.main()