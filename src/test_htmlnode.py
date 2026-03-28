import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        children = [HTMLNode("p", "Some paragraph")]
        node = HTMLNode("a", "somevalue", children, props)
        expected = 'HTMLNode(a, somevalue, [HTMLNode(p, Some paragraph, None, )],  href="https://www.google.com" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_props_to_html_empty(self):
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

    def test_leaf_to_html_tag_missing(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("a", "somevalue", props)
        expected = 'LeafNode(a, somevalue,  href="https://www.google.com" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_empty_leaf_value(self):
        with self.assertRaises(ValueError) as e:
            node = LeafNode("a", None)
            node.to_html()
        self.assertIn("leaf node must have a value", str(e.exception))

    def test_img_renders_with_src_and_alt(self):
        node = LeafNode("img", None, {"src": "https://example.com/pic.png", "alt": "example"})
        html = node.to_html()
        self.assertEqual(
            html,
            '<img src="https://example.com/pic.png" alt="example">'
        )

    def test_img_has_leading_space_before_first_attribute(self):
        node = LeafNode("img", None, {"src": "a.png"})
        html = node.to_html()
        self.assertTrue(html.startswith('<img '))
    
    def test_img_does_not_have_closing_tag(self):
        node = LeafNode("img", None, {"src": "a.png"})
        html = node.to_html()
        self.assertNotIn("</img>", html)

    def test_img_with_multiple_props_order_consistent(self):
        node = LeafNode("img", None, {"src": "a.png", "alt": "A"})
        html = node.to_html()
        self.assertIn('src="a.png"', html)
        self.assertIn('alt="A"', html)

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

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b", "bold child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>bold child</b></div>")

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError) as e:
            parent_node = ParentNode("div", None)
            parent_node.to_html()
        self.assertIn("parent node must have children", str(e.exception))

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError) as e:
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, child_node)
            parent_node.to_html()
        self.assertIn("parent node must have tag", str(e.exception))

if __name__ == "__main__":
    unittest.main()