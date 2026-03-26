import unittest

from textnode import TextNode, TextType
from splitters import split_nodes_delimiter, split_nodes_image, split_nodes_link


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


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_text(self):
        node = TextNode(
            "This text doesn't have a single image in the entire thing!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text doesn't have a single image in the entire thing!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This ![crap](https://not.real.picture/empty.png) doesn't even exist!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This ", TextType.TEXT),
                TextNode("crap", TextType.IMAGE, "https://not.real.picture/empty.png"),
                TextNode(" doesn't even exist!", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_only_text(self):
        node = TextNode(
            "This text doesn't have a single link in the entire thing!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text doesn't have a single link in the entire thing!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_only_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This link to [some fake website](https://not.real.website) is so broken!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("This link to ", TextType.TEXT),
                TextNode("some fake website", TextType.LINK, "https://not.real.website"),
                TextNode(" is so broken!", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()