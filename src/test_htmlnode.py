import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()