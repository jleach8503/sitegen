import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_nourl(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertIsNone(node.url)

    def test_urlpresent(self):
        link = "https://www.google.com"
        node = TextNode("This is a link node", TextType.LINK, link)
        self.assertEqual(node.url, link)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_bold(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com/mypic.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.google.com/mypic.png")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_invalid_type(self):
        with self.assertRaises(ValueError) as e:
            node = TextNode("This is an invalid node", "superduper")
            text_node_to_html_node(node)
        self.assertIn("invalid text_type: superduper", str(e.exception))


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        with self.assertRaises(ValueError) as e:
            nodes = [
                TextNode("This is a text node", TextType.TEXT),
            ]
            split_nodes_delimiter(nodes, "", TextType.TEXT)
        self.assertIn("a delimiter must be provided", str(e.exception))

    def test_invalid_type(self):
        with self.assertRaises(ValueError) as e:
            nodes = [
                TextNode("This is a text node", TextType.TEXT),
            ]
            split_nodes_delimiter(nodes, "*", "superduper")
        self.assertIn("invalid text_type: superduper", str(e.exception))

    def test_non_text_type(self):
        nodes = [
            TextNode("This is a bold node", TextType.BOLD),
            TextNode("This is an italic node", TextType.ITALIC),
        ]
        split_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        texts = [node.text for node in split_nodes]
        self.assertEqual(len(split_nodes), 2)
        self.assertEqual(
            texts,
            [
                "This is a bold node",
                "This is an italic node",
            ]
        )
        self.assertIs(split_nodes[0].text_type, TextType.BOLD)
        self.assertIs(split_nodes[1].text_type, TextType.ITALIC)

    def test_bold_type(self):
        nodes = [
            TextNode("This is text with a **bold** word", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        texts = [node.text for node in split_nodes]
        self.assertEqual(len(split_nodes), 3)
        self.assertEqual(
            texts,
            [
                "This is text with a ",
                "bold",
                " word",
            ]
        )
        self.assertIs(split_nodes[0].text_type, TextType.TEXT)
        self.assertIs(split_nodes[1].text_type, TextType.BOLD)
        self.assertIs(split_nodes[2].text_type, TextType.TEXT)

    def test_italic_type(self):
        nodes = [
            TextNode("_All text is italics!_", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        texts = [node.text for node in split_nodes]
        self.assertEqual(len(split_nodes), 1)
        self.assertEqual(
            texts,
            [
                "All text is italics!",
            ]
        )
        self.assertIs(split_nodes[0].text_type, TextType.ITALIC)

    def test_code_type(self):
        nodes = [
            TextNode("PowerShell cmdlet: `Get-ChildItem`", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        texts = [node.text for node in split_nodes]
        self.assertEqual(len(split_nodes), 2)
        self.assertEqual(
            texts,
            [
                "PowerShell cmdlet: ",
                "Get-ChildItem",
            ]
        )
        self.assertIs(split_nodes[0].text_type, TextType.TEXT)
        self.assertIs(split_nodes[1].text_type, TextType.CODE)


if __name__ == "__main__":
    unittest.main()