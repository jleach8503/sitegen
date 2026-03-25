import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()